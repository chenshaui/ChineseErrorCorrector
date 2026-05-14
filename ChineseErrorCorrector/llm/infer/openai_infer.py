"""
通过 OpenAI 兼容接口调用 4B 大模型（推荐 vLLM serve 部署）。
本仓库的推理主链路只依赖该接口，不再本地加载 4B 大模型权重。

`self.prompt_prefix` 与历史版本保持一致，便于复用既有的 Prompt 行为。
"""
from __future__ import annotations

import asyncio
from typing import Iterable

from openai import AsyncOpenAI, OpenAI

from ChineseErrorCorrector.config import TextCorrectConfig


class OpenAITextCorrectInfer(object):
    """通过 OpenAI 兼容接口调用部署好的 4B 纠错大模型。"""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        concurrency: int | None = None,
    ) -> None:
        self.prompt_prefix = "你是一个文本纠错专家，纠正输入句子中的语法错误，并输出正确的句子，输入句子为："

        self.base_url = base_url or TextCorrectConfig.OPENAI_BASE_URL
        self.api_key = api_key or TextCorrectConfig.OPENAI_API_KEY
        self.model = model or TextCorrectConfig.OPENAI_MODEL
        self.concurrency = int(concurrency or TextCorrectConfig.CONCURRENCY)

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
        return [{"role": "user", "content": self.prompt_prefix + sentence}]

    def _extract_text(self, completion) -> str:
        if not completion.choices:
            return ""
        message = completion.choices[0].message
        content = getattr(message, "content", "") or ""
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
