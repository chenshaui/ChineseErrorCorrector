"""
通过 OpenAI 兼容接口调用 4B 大模型（推荐 vLLM serve 部署）。
本仓库的推理主链路只依赖该接口，不再本地加载 4B 大模型权重。

同时兼容两代纠错模型：
- v3：ChineseErrorCorrector3-4B —— 直接输出纠正后的句子。
- v4：ChineseErrorCorrector4-4B（ACL 2026 Main） —— 输出
       `<think>错误类型 + 修改原因</think>\\n纠正后的句子`。本类会：
       1) 在 `infer()` 接口中自动剥掉思考块，仅返回纠正后的句子（与 v3 兼容）；
       2) 在 `infer_detailed()` 接口中返回结构化 dict：
          `{text, error_type, error_reason}`，便于上游展示错误类型与原因。

`self.prompt_prefix` 仍为类属性，按当前模型版本解析为对应的 prompt（v3 与历史一致）。
"""
from __future__ import annotations

import asyncio
import re
from typing import Iterable, TypedDict

from openai import AsyncOpenAI, OpenAI

from ChineseErrorCorrector.config import TextCorrectConfig

# <think>...</think> 思考块；允许跨行，贪婪到最近的闭合。
_THINK_BLOCK_RE = re.compile(r"<think>(.*?)</think>", re.DOTALL | re.IGNORECASE)
# 容错：若模型只吐了 <think>... 没有 </think>，丢弃 <think> 起之后的内容。
_UNCLOSED_THINK_RE = re.compile(r"<think>.*\Z", re.DOTALL | re.IGNORECASE)
# 错误类型：取一行（到换行为止），中英文冒号都接。
_ERROR_TYPE_RE = re.compile(r"错误类型\s*[：:]\s*([^\n\r]+)")
# 修改原因：贪婪到 think 块末尾或遇到下一个明显字段（如 "纠正后" / "错误类型" 再次出现）。
_ERROR_REASON_RE = re.compile(
    r"修改原因\s*[：:]\s*(.+?)(?=\n\s*(?:错误类型|纠正后|修改后)\s*[：:]|\Z)",
    re.DOTALL,
)


class CorrectResult(TypedDict, total=False):
    text: str
    error_type: str | None
    error_reason: str | None


def resolve_model_version(model_name: str, configured: str = "auto") -> str:
    """根据配置 / 模型名解析使用 v3 还是 v4 的 prompt 与输出处理逻辑。"""
    v = (configured or "auto").strip().lower()
    if v in {"v3", "v4"}:
        return v
    # auto：根据模型名识别。包含 "4-4b" / "corrector4" / "cec4" 视为 v4，其余视为 v3。
    lower = (model_name or "").lower()
    if "4-4b" in lower or "corrector4" in lower or "cec4" in lower:
        return "v4"
    return "v3"


def strip_think_block(text: str) -> str:
    """去掉 <think>...</think> 思考块，返回纠正后的句子（适配 v4 输出）。"""
    if not text:
        return ""
    cleaned = _THINK_BLOCK_RE.sub("", text)
    if "<think>" in cleaned.lower():
        cleaned = _UNCLOSED_THINK_RE.sub("", cleaned)
    return cleaned.strip()


def parse_v4_output(raw: str) -> CorrectResult:
    """
    解析 v4 输出，提取「纠正后句子 / 错误类型 / 修改原因」。
    若没有 <think> 块（例如 v3 输出或 v4 未触发思考），error_type / error_reason 返回 None。
    """
    if not raw:
        return {"text": "", "error_type": None, "error_reason": None}

    m = _THINK_BLOCK_RE.search(raw)
    if not m:
        # 无成对 think；可能是 v3 或未闭合的 v4 输出。先做兜底剥离再返回纯文本。
        return {
            "text": strip_think_block(raw),
            "error_type": None,
            "error_reason": None,
        }

    think_body = m.group(1)
    # </think> 之后的内容就是纠正后的句子（去掉前后空白）。
    after = raw[m.end():].strip()

    et_match = _ERROR_TYPE_RE.search(think_body)
    er_match = _ERROR_REASON_RE.search(think_body)
    return {
        "text": after,
        "error_type": et_match.group(1).strip() if et_match else None,
        "error_reason": er_match.group(1).strip() if er_match else None,
    }


def parse_v3_output(raw: str) -> CorrectResult:
    """v3 输出就是纠正后句子本身，结构对齐 v4 以便上游统一处理。"""
    return {
        "text": (raw or "").strip(),
        "error_type": None,
        "error_reason": None,
    }


class OpenAITextCorrectInfer(object):
    """通过 OpenAI 兼容接口调用部署好的 4B 纠错大模型。"""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        concurrency: int | None = None,
        model_version: str | None = None,
    ) -> None:
        self.base_url = base_url or TextCorrectConfig.OPENAI_BASE_URL
        self.api_key = api_key or TextCorrectConfig.OPENAI_API_KEY
        self.model = model or TextCorrectConfig.OPENAI_MODEL
        self.concurrency = int(concurrency or TextCorrectConfig.CONCURRENCY)

        self.model_version = resolve_model_version(
            self.model,
            model_version if model_version is not None else TextCorrectConfig.MODEL_VERSION,
        )
        prompts = TextCorrectConfig.PROMPTS
        if self.model_version not in prompts:
            raise ValueError(
                f"未知模型版本 {self.model_version!r}，请在 TextCorrectConfig.PROMPTS 中补充对应 prompt。"
            )
        self.prompt_prefix = prompts[self.model_version]

        self._client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=TextCorrectConfig.REQUEST_TIMEOUT,
        )
        self._async_client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=TextCorrectConfig.REQUEST_TIMEOUT,
        )

    def _build_messages(self, sentence: str) -> list[dict]:
        if self.model_version == "v4":
            # v4 的 prompt 来自 SFT instruction，句子另起一行更稳。
            return [{"role": "user", "content": f"{self.prompt_prefix}\n{sentence}"}]
        # v3：prompt + 句子 直接拼接（与历史一致，不要变）。
        return [{"role": "user", "content": self.prompt_prefix + sentence}]

    def _parse_completion(self, completion) -> CorrectResult:
        if not completion.choices:
            return {"text": "", "error_type": None, "error_reason": None}
        message = completion.choices[0].message
        content = getattr(message, "content", "") or ""
        if self.model_version == "v4":
            return parse_v4_output(content)
        return parse_v3_output(content)

    # ---- 同步接口 ----

    def infer_one(self, sentence: str) -> str:
        """返回纠正后的句子（与历史接口一致）。"""
        return self.infer_one_detailed(sentence)["text"]

    def infer_one_detailed(self, sentence: str) -> CorrectResult:
        """返回 {text, error_type, error_reason}。v3 时后两项为 None。"""
        completion = self._client.chat.completions.create(
            model=self.model,
            messages=self._build_messages(sentence),
            max_tokens=TextCorrectConfig.MAX_TOKENS,
            temperature=TextCorrectConfig.TEMPERATURE,
            seed=TextCorrectConfig.SEED,
        )
        return self._parse_completion(completion)

    def infer(self, input_list: Iterable[str]) -> list[str]:
        """同步批量推理，返回纠正后的句子列表（与历史接口一致）。"""
        return [r["text"] for r in self.infer_detailed(list(input_list))]

    def infer_detailed(self, input_list: Iterable[str]) -> list[CorrectResult]:
        """同步批量推理，返回 [{text, error_type, error_reason}, ...]。"""
        return asyncio.run(self.ainfer_detailed(list(input_list)))

    # ---- 异步接口 ----

    async def _ainfer_one_detailed(self, sentence: str, sem: asyncio.Semaphore) -> CorrectResult:
        async with sem:
            completion = await self._async_client.chat.completions.create(
                model=self.model,
                messages=self._build_messages(sentence),
                max_tokens=TextCorrectConfig.MAX_TOKENS,
                temperature=TextCorrectConfig.TEMPERATURE,
                seed=TextCorrectConfig.SEED,
            )
            return self._parse_completion(completion)

    async def ainfer(self, input_list: list[str]) -> list[str]:
        return [r["text"] for r in await self.ainfer_detailed(input_list)]

    async def ainfer_detailed(self, input_list: list[str]) -> list[CorrectResult]:
        sem = asyncio.Semaphore(self.concurrency)
        tasks = [self._ainfer_one_detailed(s, sem) for s in input_list]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    pass
