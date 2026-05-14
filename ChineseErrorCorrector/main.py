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

    def infer(self, input_list):
        if self.detector is None:
            outputs = self.llm_correct.infer(input_list)
            return res_format(input_list, outputs)

        gate_rows = self.detector.infer(input_list)
        to_fix_idx = [i for i, row in enumerate(gate_rows) if row.get("need_correct")]
        outputs = list(input_list)
        if to_fix_idx:
            to_fix = [input_list[i] for i in to_fix_idx]
            corrected = self.llm_correct.infer(to_fix)
            for idx, fixed in zip(to_fix_idx, corrected):
                outputs[idx] = fixed
        return res_format(input_list, outputs)


if __name__ == '__main__':
    infer_enginer = ErrorCorrect()

    input_text = [
        "对待每一项工作都要一丝不够。",
        "大约半个小时左右"
    ]
    result = infer_enginer.infer(input_text)
    print(result)
