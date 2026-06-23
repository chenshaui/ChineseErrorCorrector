# Chinese Spelling and Grammar Correction


<div align="center">
  <a href="https://github.com/TW-NLP/ChineseErrorCorrector">
    <img src="images/image_fx_.jpg" alt="Logo" height="156">
  </a>
</div>

---

## Introduction

This project supports Chinese spelling and grammar error correction. We have also open-sourced an [augmentation tool for spelling and grammar errors](https://github.com/TW-NLP/ChineseErrorCorrector/tree/0.1.0), large model training code, and a collection of [related papers on text correction](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/README_paper.md). We are honored to have won the CCL 2024 championship 🏆 ([view paper](https://aclanthology.org/2024.ccl-3.31/)), the [2023 NLPCC-NaCGEC Correction Task championship 🏆](https://www.google.com/search?q=https://github.com/TW-NLP/ChineseErrorCorrector%3Ftab%3Dreadme-ov-file%23nacgec-dataset), and the [2022 FCGEC Correction Task championship 🏆](https://www.google.com/search?q=https://github.com/TW-NLP/ChineseErrorCorrector%3Ftab%3Dreadme-ov-file%23fcgec-dataset). If you find this project helpful, please give it a star ✨.

## 🔥🔥🔥 News

\[2025/08/08] Released a [general-purpose text evaluation tool](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/ChineseErrorCorrector/scores/README.md) 🎉, which allows for text correction evaluation even with low resources.

\[2025/08/06] Published a [continuously updated list of papers related to text correction](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/README_paper.md) 🥳, to facilitate research and study.

\[2025/08/01] Released [twnlp/ChineseErrorCorrector3-4B](https://huggingface.co/twnlp/ChineseErrorCorrector3-4B) 🎉🎉🎉, with comprehensively improved generalization capabilities. It ranks first among all open-source models. [See the leaderboard for details](https://www.google.com/search?q=https://github.com/TW-NLP/ChineseErrorCorrector%3Ftab%3Dreadme-ov-file%23evaluation).

\[2025/05/01] Based on a [suggestion](https://github.com/TW-NLP/ChineseErrorCorrector/issues/17), we have retrained the correction model (ChineseErrorCorrector2-7B) and have completely open-sourced the training steps to support result reproducibility. [See the tutorial for reproduction](https://www.google.com/search?q=https://github.com/TW-NLP/ChineseErrorCorrector/tree/v0.4.0%3Ftab%3Dreadme-ov-file%23reproducing-experimental-results).

\[2025/03/17] Updated batch processing for incorrect text. See [transformers batch inference](https://www.google.com/search?q=https://github.com/TW-NLP/ChineseErrorCorrector%3Ftab%3Dreadme-ov-file%23transformers-batch-inference) and [VLLM batch inference](https://www.google.com/search?q=https://github.com/TW-NLP/ChineseErrorCorrector%3Ftab%3Dreadme-ov-file%23vllm-asynchronous-batch-inference).

\[2025/03/10] The model now supports multiple inference methods, including transformers, VLLM, and modelscope.

\[2025/02/25] 🎉🎉🎉 After multiple rounds of iterative training on 2 million correction data points, we released [twnlp/ChineseErrorCorrector2-7B](https://huggingface.co/twnlp/ChineseErrorCorrector2-7B). On the [official NaCGEC-2023NLPCC test set](https://github.com/masr2000/NaCGEC), it surpassed the first-place model from Huawei by 10 points, taking a significant lead. [Technical details](https://blog.csdn.net/qq_43765734/article/details/145858955).

\[2025/02] For easier deployment, we released [twnlp/ChineseErrorCorrector-1.5B](https://huggingface.co/twnlp/ChineseErrorCorrector-1.5B), trained on 380,000 open-source spelling data points.

\[2025/01] Using 380,000 open-source spelling data points and based on Qwen2.5, we trained a Chinese spelling correction model that supports corrections for phonologically and visually similar characters, releasing [twnlp/ChineseErrorCorrector-7B](https://huggingface.co/twnlp/ChineseErrorCorrector-7B) and [twnlp/ChineseErrorCorrector-32B-LORA](https://huggingface.co/twnlp/ChineseErrorCorrector-32B-LORA/tree/main).

\[2024/06] v0.1.0 release: 🎉🎉🎉 Open-sourced a one-click grammatical error augmentation tool. This tool can augment text with 14 types of grammatical errors. Users in different fields can use their own data to replace errors and train custom grammar and spelling models. See [Tag-v0.1.0](https://github.com/TW-NLP/ChineseErrorCorrector/tree/0.1.0) for details.

## Model List

| Model Name                                                                                  | Correction Type    | Description                                                                                                                                                                |
| :------------------------------------------------------------------------------------------ | :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [twnlp/ChineseErrorCorrector3-4B](https://huggingface.co/twnlp/ChineseErrorCorrector3-4B)   | Grammar + Spelling | Fully trained on 2 million correction data points. Suitable for both grammar and spelling correction. Best performance, recommended for use.                               |
| [twnlp/ChineseErrorCorrector2-7B](https://huggingface.co/twnlp/ChineseErrorCorrector2-7B)   | Grammar + Spelling | Trained with multiple iterative rounds on 2 million correction data points. Suitable for grammar and spelling correction, with good performance.                           |
| [twnlp/ChineseErrorCorrector-7B](https://huggingface.co/twnlp/ChineseErrorCorrector-7B)     | Spelling           | Trained on 380,000 open-source spelling data points. Supports correction of phonologically and visually similar character errors. Good performance on spelling correction. |
| [twnlp/ChineseErrorCorrector-1.5B](https://huggingface.co/twnlp/ChineseErrorCorrector-1.5B) | Spelling           | Trained on 380,000 open-source spelling data points. Supports correction of phonologically and visually similar character errors. Fair performance on spelling correction. |

## Datasets

| Dataset Name              | Data Link                                                                                        | Size and Category                                                        | Description                                             |
| :------------------------ | :----------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :------------------------------------------------------ |
| ChinseseErrorCorrectData  | [twnlp/ChinseseErrorCorrectData](https://huggingface.co/datasets/twnlp/ChinseseErrorCorrectData) | 2 million                                                                | Training dataset for ChineseErrorCorrector2-7B.         |
| CSC (Spelling Correction) | [twnlp/csc\_data](https://huggingface.co/datasets/twnlp/csc_data)                                | W271K(279,816) Medical(39,303) Lemon(22,259) ECSpell(6,688) CSCD(35,001) | Chinese spelling correction datasets.                   |
| CGC (Grammar Correction)  | [twnlp/cgc\_data](https://huggingface.co/datasets/twnlp/cgc_data)                                | CGED(20,449) FCGEC(37,354) MuCGEC(2,467) NaCGEC(7,568)                   | Chinese grammar correction datasets.                    |
| Lang8+HSK                 | [twnlp/lang8\_hsk](https://huggingface.co/datasets/twnlp/lang8_hsk)                              | 1,568,885                                                                | A mixed dataset of Chinese spelling and grammar errors. |

## Evaluation (Generalization)

### Evaluation Results

* **Evaluation Metric**: F1
* **CSC (Chinese Spelling Correction)**: Models that can handle aligned errors such as those based on phonological or visual similarity.
* **CTC (Chinese Text Correction)**: Models that support spelling and grammar corrections, including unaligned errors like extra or missing characters.
* **GPU**: Tesla V100, 32 GB VRAM

| Model Name                  | Model Link                                                                                                              | Base Model                     | Avg        | SIGHAN-2015 | EC-LAW | MCSC   | GPU | QPS     |
| :-------------------------- | :---------------------------------------------------------------------------------------------------------------------- | :----------------------------- | :--------- | :---------- | :----- | :----- | :-- | :------ |
| Kenlm-CSC                   | [shibing624/chinese-kenlm-klm](https://huggingface.co/shibing624/chinese-kenlm-klm)                                     | kenlm                          | 0.3409     | 0.3147      | 0.3763 | 0.3317 | CPU | 9       |
| Mengzi-T5-CSC               | [shibing624/mengzi-t5-base-chinese-correction](https://huggingface.co/shibing624/mengzi-t5-base-chinese-correction)     | mengzi-t5-base                 | 0.3984     | 0.7758      | 0.3156 | 0.1039 | GPU | 214     |
| ERNIE-CSC                   | [PaddleNLP/ernie-csc](https://github.com/PaddlePaddle/PaddleNLP/tree/develop/legacy/examples/text_correction/ernie-csc) | PaddlePaddle/ernie-1.0-base-zh | 0.4353     | 0.8383      | 0.3357 | 0.1318 | GPU | 114     |
| MacBERT-CSC                 | [shibing624/macbert4csc-base-chinese](https://huggingface.co/shibing624/macbert4csc-base-chinese)                       | hfl/chinese-macbert-base       | 0.3993     | 0.8314      | 0.1610 | 0.2055 | GPU | **224** |
| ChatGLM3-6B-CSC             | [shibing624/chatglm3-6b-csc-chinese-lora](https://huggingface.co/shibing624/chatglm3-6b-csc-chinese-lora)               | THUDM/chatglm3-6b              | 0.4538     | 0.6572      | 0.4369 | 0.2672 | GPU | 3       |
| Qwen2.5-1.5B-CTC            | [shibing624/chinese-text-correction-1.5b](https://huggingface.co/shibing624/chinese-text-correction-1.5b)               | Qwen/Qwen2.5-1.5B-Instruct     | 0.6802     | 0.3032      | 0.7846 | 0.9529 | GPU | 6       |
| Qwen2.5-7B-CTC              | [shibing624/chinese-text-correction-7b](https://huggingface.co/shibing624/chinese-text-correction-7b)                   | Qwen/Qwen2.5-7B-Instruct       | 0.8225     | 0.4917      | 0.9798 | 0.9959 | GPU | 3       |
| \*\*Q**Qwen3-4B-CTC (Our)** | [twnlp/ChineseErrorCorrector3-4B](https://huggingface.co/twnlp/ChineseErrorCorrector3-4B)                               | Qwen/Qwen3-4B                  | **0.8521** | 0.6340      | 0.9360 | 0.9864 | GPU | 5       |

## Text Correction Competition Evaluation (Two-Time Champions 🏆)

### NaCGEC Dataset

* **Evaluation Tool**: ChERRANT [Evaluation Tool](https://github.com/HillZhang1999/MuCGEC)
* **Evaluation Data**: [NaCGEC](https://github.com/masr2000/NaCGEC)
* **Evaluation Metric**: F1-0.5

🏆

| Model Name                                     | Model Link                                                                                                                                                               | Prec   | Rec    | F0.5   |
| :--------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :----- | :----- |
| twnlp/ChineseErrorCorrector3-4B                | [huggingface](https://huggingface.co/twnlp/ChineseErrorCorrector3-4B) ; [modelscope(China download)](https://www.modelscope.cn/models/tiannlp/ChineseErrorCorrector3-4B) | 0.542  | 0.3475 | 0.4874 |
| HW\_TSC\_nlpcc2023\_cgec (Huawei)              | Not open-sourced                                                                                                                                                         | 0.5095 | 0.3129 | 0.4526 |
| 鱼饼啾啾Plus (Peking University)                   | Not open-sourced                                                                                                                                                         | 0.5708 | 0.1294 | 0.3394 |
| CUHK\_SU (The Chinese University of Hong Kong) | Not open-sourced                                                                                                                                                         | 0.3882 | 0.1558 | 0.2990 |

### FCGEC Dataset

* \*\***Evaluation Metric**: binary\_f1

[Evaluation 🏆]([https://codalab.lisn.upsaclay.fr/competitions/8020#]%28https://www.google.com/search?q=https://codalab.lisn.upsaclay.fr/competitions/8020%23%29https://codalab.lisn.upsaclay.fr/competitions/8020#results)

## Usage

### 🤗 transformers

```shell
pip install transformers
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
set_seed(42)

model_name = "twnlp/ChineseErrorCorrector3-4B"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "You are a text correction expert. Correct the grammatical errors in the input sentence and output the corrected sentence. The input sentence is: "
text_input = "对待每一项工作都要一丝不够。" # Incorrect: "Approach every task with a thread of not enough."
messages = [
    {"role": "user", "content": prompt + text_input}
]
text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
    )
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response) # Corrected output: 对待每一项工作都要一丝不苟。 (Approach every task meticulously.)
```

### VLLM

```shell
pip install transformers
pip install vllm==0.8.5
```

```python
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained("twnlp/ChineseErrorCorrector3-4B")

# Pass the default decoding hyperparameters of twnlp/ChineseErrorCorrector3-4B
# max_tokens is for the maximum length for generation.
sampling_params = SamplingParams(seed=42, max_tokens=512)

# Input the model name or path. Can be GPTQ or AWQ models.
llm = LLM(model="twnlp/ChineseErrorCorrector3-4B")

# Prepare your prompts
text_input = "对待每一项工作都要一丝不够。" # Incorrect
messages = [
    {"role": "user", "content": "You are a text correction expert. Correct the grammatical errors in the input sentence and output the corrected sentence. The input sentence is: " + text_input}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False
)

# generate outputs
outputs = llm.generate([text], sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

### VLLM Asynchronous Batch Inference (Recommended for Production)

* Clone the repo

<!-- end list -->

```sh
git clone https://github.com/TW-NLP/ChineseErrorCorrector
cd ChineseErrorCorrector
```

* Install Conda: please see [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
* Create Conda env:

<!-- end list -->

```sh
conda create -n zh_correct -y python=3.10
conda activate zh_correct
pip install -r requirements.txt
# If you are in mainland China, you can use a mirror:
# pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

```sh
# Modify config.py
# (1) Change DEFAULT_CKPT_PATH according to your model. Default is twnlp/ChineseErrorCorrector3-4B.
#     (Download the model and place it in ChineseErrorCorrector/pre_model/twnlp/ChineseErrorCorrector3-4B)
# (2) Set TextCorrectConfig's USE_VLLM = True

# Batch prediction
python main.py
```

### Transformers Batch Inference

* Clone the repo

<!-- end list -->

```sh
git clone https://github.com/TW-NLP/ChineseErrorCorrector
cd ChineseErrorCorrector
```

* Install Conda: please see [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
* Create Conda env:

<!-- end list -->

```sh
conda create -n zh_correct -y python=3.10
conda activate zh_correct
pip install -r requirements.txt
# If you are in mainland China, you can use a mirror:
# pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

```sh
# Modify config.py
# (1) Change DEFAULT_CKPT_PATH according to your model. Default is twnlp/ChineseErrorCorrector3-4B.
# (2) Set TextCorrectConfig's USE_VLLM = False

# Batch prediction
python main.py

# Output:
'''
[{'source': '对待每一项工作都要一丝不够。', 'target': '对待每一项工作都要一丝不苟。', 'errors': [('够', '苟', 12)]}, {'source': '大约半个小时左右', 'target': '大约半个小时', 'errors': [('左右', '', 6)]}]
'''
```

### 🤖 modelscope

```shell
pip install modelscope
```

```python
from modelscope import AutoModelForCausalLM, AutoTokenizer

model_name = "tiannlp/ChineseErrorCorrector3-4B" # Note the model name is slightly different on modelscope

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "You are a text correction expert. Correct the grammatical errors in the input sentence and output the corrected sentence. The input sentence is: "
text_input = "对待每一项工作都要一丝不够。" # Incorrect
messages = [
    {"role": "user", "content": prompt + text_input}
]
text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
    )
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response) # Corrected output
```

## Citation

If this work is helpful, please kindly cite as:

```bibtex
@inproceedings{wei2024中小学作文语法错误检测,
  title={Research on Automated Methods for Grammatical Error Detection, Sentence Revision, and Fluency Rating in Primary and Secondary School Compositions},
  author={Wei, Tian},
  booktitle={Proceedings of the 23rd Chinese National Conference on Computational Linguistics (Volume 3: Evaluations)},
  pages={278--284},
  year={2024}
}
```

## Contributing

Contributions of all kinds are welcome: reporting issues, improving documentation, adding data, fixing bugs, and submitting new features. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the Issue / Pull Request guidelines and code style before you start.

## License

This project is released under the [Apache-2.0 License](LICENSE). You are free to use it for research and commercial purposes; please retain the copyright and license notices.

## References

* [pycorrector (Chinese Corrector System)](https://github.com/shibing624/pycorrector)
* [Chinese-text-correction-papers (A list of papers on correction)](https://github.com/nghuyong/Chinese-text-correction-papers)
