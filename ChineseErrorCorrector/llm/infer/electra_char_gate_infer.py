"""
轻量字级「是否可能出错」推理头（ELECTRA TokenClassification），与主仓库
`ErrorCorrect.hf_infer / vllm_infer` 的输入形式一致：list[str] 原句。

输出为结构化 dict，字段与 docskill 字级流水线 `pipeline_char.py` 的 JSON 行一致，
便于在大模型纠错前做门控，减少无效调用。

使用方式（放在本仓库 ChineseErrorCorrector 包内后）::

    from ChineseErrorCorrector.llm.infer.electra_char_gate_infer import ElectraCharGateInfer

    gate = ElectraCharGateInfer(
        model_name_or_path="你的HF用户名/chinese-char-error-detector-electra",
        sentence_threshold=0.5,
    )
    rows = gate.infer(["对待每一项工作都要一丝不够。", "大约半个小时左右"])

依赖：torch, transformers；需 Fast tokenizer（与训练时一致）。
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForTokenClassification, AutoTokenizer

from ChineseErrorCorrector.config import DEVICE


def _normalize_text(text: str) -> str:
    """与 docskill `normalize.normalize_text` 一致：NFKC + 空白折叠。"""
    if text is None:
        return ""
    s = unicodedata.normalize("NFKC", str(text))
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s


def _offsets_batch_to_lists(offset: Any) -> list[list[tuple[int, int]]]:
    if isinstance(offset, torch.Tensor):
        arr = offset.cpu().numpy()
        if arr.ndim == 2:
            return [[tuple(map(int, row)) for row in arr]]
        return [[tuple(map(int, row)) for row in seq] for seq in arr]
    if isinstance(offset, list):
        out: list[list[tuple[int, int]]] = []
        for row in offset:
            if isinstance(row, torch.Tensor):
                r = row.cpu().numpy()
                out.append([tuple(map(int, x)) for x in r])
            else:
                out.append([(int(t[0]), int(t[1])) for t in row])
        return out
    raise TypeError(f"不支持的 offset_mapping 类型: {type(offset)}")


def _decode_char_level_for_one(
    text: str,
    off_list: list[tuple[int, int]],
    logits: np.ndarray,
) -> tuple[int, np.ndarray, np.ndarray, np.ndarray]:
    probs = F.softmax(torch.from_numpy(logits), dim=-1).numpy()
    p_err = probs[:, 1]
    pred_tok = logits.argmax(axis=-1)

    char_end = 0
    for s, e in off_list:
        if s == 0 and e == 0:
            continue
        char_end = max(char_end, e)

    char_end = min(char_end, len(text))
    char_pred = np.zeros(char_end, dtype=np.int64)
    char_max_p = np.zeros(char_end, dtype=np.float32)

    for j, (st, en) in enumerate(off_list):
        if st == 0 and en == 0:
            continue
        st = min(int(st), char_end)
        en = min(int(en), char_end)
        if st >= en:
            continue
        if pred_tok[j] == 1:
            char_pred[st:en] = 1
        char_max_p[st:en] = np.maximum(char_max_p[st:en], float(p_err[j]))

    return char_end, char_pred, char_max_p, pred_tok


@torch.inference_mode()
def _forward_char_preds_batch(
    texts: list[str],
    model: Any,
    tokenizer: Any,
    device: torch.device,
    max_length: int,
) -> list[tuple[int, np.ndarray, np.ndarray, np.ndarray]]:
    if not texts:
        return []
    enc = tokenizer(
        list(texts),
        max_length=max_length,
        truncation=True,
        padding=True,
        return_offsets_mapping=True,
        return_tensors="pt",
    )
    offset = enc.pop("offset_mapping")
    off_lists = _offsets_batch_to_lists(offset)
    enc = {k: v.to(device) for k, v in enc.items()}
    logits = model(**enc).logits.float().cpu().numpy()
    out: list[tuple[int, np.ndarray, np.ndarray, np.ndarray]] = []
    for i, text in enumerate(texts):
        out.append(_decode_char_level_for_one(text, off_lists[i], logits[i]))
    return out


class ElectraCharGateInfer:
    """
    字级检错门控：输入与 `ErrorCorrect` 相同的句子列表；输出每条句子的
    need_correct / 字级 0-1 串 / 最大错字概率等。
    """

    def __init__(
        self,
        model_name_or_path: str,
        *,
        device: str | torch.device | None = None,
        max_length: int = 256,
        sentence_threshold: float = 0.5,
        batch_size: int = 32,
    ) -> None:
        self.sentence_threshold = float(sentence_threshold)
        self.max_length = int(max_length)
        self.batch_size = max(1, int(batch_size))
        dev = device if device is not None else DEVICE
        self._device = torch.device(dev)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
        if not getattr(self.tokenizer, "is_fast", False):
            raise RuntimeError("字级门控需要 Fast tokenizer（return_offsets_mapping）")
        self.model = AutoModelForTokenClassification.from_pretrained(model_name_or_path)
        self.model.eval().to(self._device)

    def infer(self, input_list: list[str]) -> list[dict[str, Any]]:
        """
        :param input_list: 与 `ErrorCorrect` 示例中相同的原句列表。
        :return: 与 `pipeline_char` 每行 JSON 对齐的 dict 列表；并额外带 `source` 键指向入参原句。
        """
        out_rows: list[dict[str, Any]] = []
        buf_texts: list[str] = []
        buf_sources: list[str] = []

        def flush() -> None:
            nonlocal buf_texts, buf_sources
            if not buf_texts:
                return
            preds = _forward_char_preds_batch(
                buf_texts, self.model, self.tokenizer, self._device, self.max_length
            )
            for src, text, (char_end, char_pred, char_max_p, _) in zip(
                buf_sources, buf_texts, preds
            ):
                max_p = float(char_max_p.max()) if len(char_max_p) else 0.0
                need = max_p >= self.sentence_threshold
                out_rows.append(
                    {
                        "source": src,
                        "text": text,
                        "need_correct": need,
                        "max_p_err": max_p,
                        "char_flags": "".join(str(int(x)) for x in char_pred.tolist()),
                        "char_end": int(char_end),
                    }
                )
            buf_texts = []
            buf_sources = []

        for raw in input_list:
            text = _normalize_text(raw)
            if not text:
                out_rows.append(
                    {
                        "source": raw,
                        "text": "",
                        "need_correct": False,
                        "max_p_err": 0.0,
                        "char_flags": "",
                        "char_end": 0,
                    }
                )
                continue
            buf_sources.append(raw)
            buf_texts.append(text)
            if len(buf_texts) >= self.batch_size:
                flush()
        flush()
        return out_rows


def filter_sources_for_llm(
    gate_rows: list[dict[str, Any]],
) -> tuple[list[str], list[int]]:
    """
    根据 gate 结果筛出建议送大模型纠错的句子；返回 (子列表, 在原 input_list 中的下标)。
    仅对 need_correct 为 True 的项保留 source（原句字符串）。
    """
    sub: list[str] = []
    idxs: list[int] = []
    for i, row in enumerate(gate_rows):
        if row.get("need_correct"):
            sub.append(row["source"])
            idxs.append(i)
    return sub, idxs


if __name__ == "__main__":
    pass
