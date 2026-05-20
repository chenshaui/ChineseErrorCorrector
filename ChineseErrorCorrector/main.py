import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ChineseErrorCorrector.config import TextCorrectConfig
from ChineseErrorCorrector.llm.infer.openai_infer import OpenAITextCorrectInfer
from ChineseErrorCorrector.utils.correct_tools import res_format


class ErrorCorrect(object):
    """
    中文拼写和语法错误纠正。

    - 主链路：通过 OpenAI 兼容接口调用 4B 大模型（vLLM serve 部署）。
    - 可选门控：ELECTRA 字级判别器，仅对疑似有错的句子调大模型，由
      `TextCorrectConfig.USE_DETECTOR` 控制（默认关闭）。

    输出结构（与历史兼容，v4 额外带 error_type / error_reason）：
        [{
            "source": 原句,
            "target": 纠正后的句子,
            "errors": [(原字, 新字, 位置), ...],
            "error_type": "错别字" | "词语搭配错误" | ... | None,   # 仅 v4 有，v3 为 None
            "error_reason": "原句中的xxx应为yyy..."            | None,   # 仅 v4 有，v3 为 None
        }, ...]
    """

    def __init__(self):
        self.llm_correct = OpenAITextCorrectInfer()
        self.detector = None
        if TextCorrectConfig.USE_DETECTOR:
            from ChineseErrorCorrector.llm.infer.electra_char_gate_infer import (
                ElectraCharGateInfer,
                get_default_detector_path,
            )

            self.detector = ElectraCharGateInfer(
                model_name_or_path=get_default_detector_path(),
                sentence_threshold=TextCorrectConfig.DETECTOR_SENTENCE_THRESHOLD,
                max_length=TextCorrectConfig.DETECTOR_MAX_LENGTH,
                batch_size=TextCorrectConfig.DETECTOR_BATCH_SIZE,
            )

    @staticmethod
    def _merge_reasoning(rows, details):
        """把 LLM detailed 输出的 error_type / error_reason 合并进 res_format 的每条结果。"""
        if rows is None:
            return rows
        for row, detail in zip(rows, details):
            row["error_type"] = detail.get("error_type")
            row["error_reason"] = detail.get("error_reason")
        return rows

    def infer(self, input_list):
        # 不启用 ELECTRA：所有句子都送大模型
        if self.detector is None:
            details = self.llm_correct.infer_detailed(input_list)
            outputs = [d["text"] for d in details]
            rows = res_format(input_list, outputs)
            return self._merge_reasoning(rows, details)

        # 启用 ELECTRA：仅疑似有错的句子送大模型
        gate_rows = self.detector.infer(input_list)
        to_fix_idx = [i for i, row in enumerate(gate_rows) if row.get("need_correct")]
        outputs = list(input_list)
        # 默认所有句子的 error_type / error_reason 为 None
        details = [
            {"text": s, "error_type": None, "error_reason": None}
            for s in input_list
        ]
        if to_fix_idx:
            to_fix = [input_list[i] for i in to_fix_idx]
            corrected_details = self.llm_correct.infer_detailed(to_fix)
            for idx, det in zip(to_fix_idx, corrected_details):
                outputs[idx] = det["text"]
                details[idx] = det
        rows = res_format(input_list, outputs)
        return self._merge_reasoning(rows, details)


if __name__ == '__main__':
    infer_enginer = ErrorCorrect()

    input_text = [
        "对待每一项工作都要一丝不够。",
        "大约半个小时左右",
    ]
    result = infer_enginer.infer(input_text)
    print(result)
