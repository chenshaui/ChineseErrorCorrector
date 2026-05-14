# ELECTRA 字级门控（可选）

中文纠错主链路里，大模型单次推理成本高、延迟大。可选模块 `ChineseErrorCorrector/llm/infer/electra_char_gate_infer.py` 提供一层轻量字级二分类：在 Chinese ELECTRA 判别器上做 TokenClassification 微调，子词对齐到字，给出「该字是否像有错」的标签与概率。在调用 ErrorCorrect 之前，可先判断句子是否值得送进大模型；明显干净的句子可跳过生成，以省算力、降延迟。

权重使用独立的 Hugging Face 模型或本地目录（与主仓库默认纠错权重无关）。需要 Fast tokenizer（`use_fast=True`，支持 offset_mapping）。基座与社区常用骨干一致：[hfl/chinese-electra-180g-base-discriminator](https://huggingface.co/hfl/chinese-electra-180g-base-discriminator)。

**官方权重（推荐）**：[xurong123/ChineseErrorDetectorElectra](https://huggingface.co/xurong123/ChineseErrorDetectorElectra)。

**数据与复现材料（Hugging Face）**
字级对齐后的训练/验证数据、生成方式说明，以及本地一键脚本对应的用法与字段说明，均已整理并发布在 Hugging Face Hub 仓库 [xurong123/ChineseErrorDetectorElectra](https://huggingface.co/xurong123/ChineseErrorDetectorElectra)：内含可复用的数据说明、样例与相关脚本入口，便于直接 datasets 加载或对照本仓库代码复现预处理流程。

## 启用方式

1. **下载权重**：从 [xurong123/ChineseErrorDetectorElectra](https://huggingface.co/xurong123/ChineseErrorDetectorElectra) 下载，**推荐**放到 `ChineseErrorCorrector/pre_model/ChineseErrorDetectorElectra/` 下（即 `config.py` 中 `DEFAULT_DETECTOR_PATH` 的默认路径）。也可设置环境变量 `CHAR_GATE_HF_REPO_ID` 指向其他本地路径或 HF 仓库 id 走在线加载。
2. **打开开关**：在 `ChineseErrorCorrector/config.py` 中把 `TextCorrectConfig.USE_DETECTOR` 改为 `True`，主链路（`ErrorCorrect.infer`）会先用门控筛句、再仅对 `need_correct == True` 的句子调用 4B 大模型 OpenAI 接口。

可调项：

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `USE_DETECTOR` | `False` | 是否启用 ELECTRA 字级门控 |
| `DEFAULT_DETECTOR_PATH` | `ChineseErrorCorrector/pre_model/ChineseErrorDetectorElectra` | 门控模型本地路径或 HF 仓库 id，可用环境变量 `CHAR_GATE_HF_REPO_ID` 覆盖 |
| `DETECTOR_SENTENCE_THRESHOLD` | `0.5` | 句级阈值（`max_p_err`） |
| `DETECTOR_MAX_LENGTH` | `256` | 最大序列长度 |
| `DETECTOR_BATCH_SIZE` | `32` | 门控 batch size |

## 加速思路

门控侧参数量远小于 4B/7B 纠错模型，且实现支持 padding batch（`batch_size` 可调）。仅对 `need_correct == True` 的句子调用 4B 大模型 OpenAI 接口，无错或风险低的句子不再走自回归生成；实际收益取决于数据中无需纠错的比例、门控阈值和大模型 batch 策略，主要来自减少生成次数。

## 数据与标签

- **训练/验证主 JSONL**：由 CEC 转换而来，每行 `{"source","target"}`；本地常见文件名 `data/cec_train.jsonl`、`data/cec_validation.jsonl`。
- **字级标签**：`char_align.py` 对归一化后的 `source`/`target` 做 `difflib.SequenceMatcher`，`replace`/`delete` 在 source 上标 **1**，其余 **0**；纯 insert 在 target 侧时 source 可能全 0，属规则定义而非实现错误。
- **分层验证集** `data/val_task_stratified.jsonl`：由 `prepare_task_validation_jsonl.py` 从 **csc / cgc** 等抽样，字段含 `task`（`spelling` / `grammar` / `mixed`）与 `corpus`。**mixed** 在 Lang8 不可用时自动回退为 **`cec_validation.jsonl`** 抽样，并在 `corpus` 中标注 `mixed_fallback:cec_validation.jsonl`。

---

## 性能量级（供参考）

### Evaluation (Quick Snapshot)

`val_task_stratified.jsonl`（7500 句，spelling/grammar/mixed 各 2500）上的一次对照实验：

| Split | ELECTRA (P / R / F1) | MacBERT (P / R / F1) | Better |
|---|---|---|---|
| Overall (char-level) | 0.256 / 0.822 / 0.391 | 0.264 / 0.797 / 0.396 | MacBERT F1 略高，ELECTRA Recall 更高 |
| Spelling (char-level) | **0.611 / 0.986 / 0.754** | 0.568 / 0.984 / 0.720 | **ELECTRA** |
| Grammar (char-level) | 0.214 / 0.823 / 0.339 | **0.225 / 0.838 / 0.355** | **MacBERT** |
| Mixed (char-level) | 0.206 / **0.732** / **0.322** | **0.210** / 0.662 / 0.319 | ELECTRA（Recall/F1） |
| Sentence gate (best F1, `max_p_err` sweep) | **0.859** | 0.854 | **ELECTRA** |

> 注：这是阶段性结果（固定一次实验配置）。上线时请在你的验证集上重新做阈值 sweep。
> 同类字级门控在公开拼写向语料上，可出现字级召回约 0.986、F1 约 0.75 量级，适合少漏检前筛；精确率相对适中，需用 `sentence_threshold`（句级 max_p_err）在漏检与多调大模型之间折中。语法与混合难例上不如拼写稳，更适合省算力而非单独替代大模型。在 A100、较大 batch（如 512～1024）、`max_length=256` 等设置下，纯 GPU 前向可达约 100+ 句/秒量级；具体以本模型验证与线上实测为准。

## 输入输出（与主仓库对齐）

与 `ErrorCorrect` 相同：入参为原句列表 `input_list: list[str]`。门控出参为字典列表，每条含 `source`、`text`（归一化后用于推理）、`need_correct`、`max_p_err`、`char_flags`、`char_end`。主链路纠错结果仍为 `res_format` 的 `source` / `target` / `errors`。

## 示例

启用门控后，直接调用 `ErrorCorrect.infer` 即可（内部会先跑门控、再调 4B 大模型 OpenAI 接口）：

```python
# 在 ChineseErrorCorrector/config.py 中设置 TextCorrectConfig.USE_DETECTOR = True
from ChineseErrorCorrector.main import ErrorCorrect

correct = ErrorCorrect()
raw = ["对待每一项工作都要一丝不够。", "大约半个小时左右"]
result = correct.infer(raw)
print(result)
```

也可以独立使用门控、自行决定送哪些句子给主链路：

```python
from ChineseErrorCorrector.main import ErrorCorrect
from ChineseErrorCorrector.llm.infer.electra_char_gate_infer import (
    CHAR_GATE_HF_REPO_ID,
    ElectraCharGateInfer,
    filter_sources_for_llm,
)

gate = ElectraCharGateInfer(model_name_or_path=CHAR_GATE_HF_REPO_ID, sentence_threshold=0.5)
correct = ErrorCorrect()

raw = ["对待每一项工作都要一丝不够。", "大约半个小时左右"]
gate_rows = gate.infer(raw)
to_fix, _ = filter_sources_for_llm(gate_rows)
llm_out = correct.llm_correct.infer(to_fix) if to_fix else []
```
