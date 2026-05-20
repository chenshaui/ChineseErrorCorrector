"""
通过 OpenAI 兼容接口调用 4B 大模型（推荐 vLLM serve 部署）。
本仓库的推理主链路只依赖该接口，不再本地加载 4B 大模型权重。

同时兼容两代纠错模型：
- v3：ChineseErrorCorrector3-4B —— 直接输出纠正后的句子。
- v4：ChineseErrorCorrector4-4B（ACL 2026 Main） —— 输出
       `<think>错误类型 + 修改原因</think>\\n纠正后的句子`，本类会自动剥掉思考块、
       只返回纠正后的句子，保证下游接口与 v3 一致。

`self.prompt_prefix` 仍为类属性，按当前模型版本解析为对应的 prompt（v3 与历史一致）。
"""
from __future__ import annotations

import asyncio
import re
from typing import Iterable

from openai import AsyncOpenAI, OpenAI

from ChineseErrorCorrector.config import TextCorrectConfig

# 匹配 <think>...</think> 思考块（贪婪到最近的闭合）；允许跨行。
_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
# 容错：若模型只吐了 <think>... 没有 </think>，按起始位置截断保留前面的部分。
_UNCLOSED_THINK_RE = re.compile(r"<think>.*\Z", re.DOTALL | re.IGNORECASE)


def resolve_model_version(model_name: str, configured: str = "auto") -> str:
    """根据配置 / 模型名解析使用 v3 还是 v4 的 prompt 与输出处理逻辑。"""
    v = (configured or "auto").strip().lower()
    if v in {"v3", "v4"}:
        return v
    # auto：根据模型名识别。包含 "4-4b" / "corrector4" 视为 v4，其余视为 v3。
    lower = (model_name or "").lower()
    if "4-4b" in lower or "corrector4" in lower or "cec4" in lower:
        return "v4"
    return "v3"


def strip_think_block(text: str) -> str:
    """去掉 <think>...</think> 思考块，返回纠正后的句子（适配 v4 输出）。"""
    if not text:
        return ""
    # 优先剥成对的 <think>...</think>
    cleaned = _THINK_BLOCK_RE.sub("", text)
    # 模型偶尔输出未闭合的思考块（截断 / 上限触发），保守做法：丢弃 <think> 起之后的内容。
    if "<think>" in cleaned.lower():
        cleaned = _UNCLOSED_THINK_RE.sub("", cleaned)
    return cleaned.strip()


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

        # 解析模型版本与对应 prompt
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
            # v4 的 prompt 来自 SFT instruction，句子放在 user 内容里另起一行更稳。
            return [{"role": "user", "content": f"{self.prompt_prefix}\n{sentence}"}]
        # v3：prompt + 句子 直接拼接（与历史一致，不要变）。
        return [{"role": "user", "content": self.prompt_prefix + sentence}]

    def _extract_text(self, completion) -> str:
        if not completion.choices:
            return ""
        message = completion.choices[0].message
        content = getattr(message, "content", "") or ""
        # v4 输出含 <think>...</think>，统一剥掉，对外接口与 v3 一致。
        if self.model_version == "v4":
            content = strip_think_block(content)
        return content.strip()

    def infer_one(self, sentence: str) -> str:
        completion = self._client.chat.completions.create(
            model=self.model,
            messages=self._build_messages(sentence),
            max_tokens=TextCorrectConfig.MAX_TOKENS,
            temperature=TextCorrectConfig.TEMPERATURE,
            seed=TextCorrectConfig.SEED,
        )
        return self._extract_text(completion)

    def infer(self, input_list: Iterable[str]) -> list[str]:
        """同步批量推理（按并发数并行调用接口）。"""
        return asyncio.run(self.ainfer(list(input_list)))

    async def _ainfer_one(self, sentence: str, sem: asyncio.Semaphore) -> str:
        async with sem:
            completion = await self._async_client.chat.completions.create(
                model=self.model,
                messages=self._build_messages(sentence),
                max_tokens=TextCorrectConfig.MAX_TOKENS,
                temperature=TextCorrectConfig.TEMPERATURE,
                seed=TextCorrectConfig.SEED,
            )
            return self._extract_text(completion)

    async def ainfer(self, input_list: list[str]) -> list[str]:
        sem = asyncio.Semaphore(self.concurrency)
        tasks = [self._ainfer_one(s, sem) for s in input_list]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    pass
