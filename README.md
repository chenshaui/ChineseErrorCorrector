# 中文拼写和语法纠错

[**🇨🇳中文**](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/README.md)   [**English**](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/README_EN.md)

<div align="center">
  <a href="https://github.com/TW-NLP/ChineseErrorCorrector">
    <img src="images/image_fx_.jpg" alt="Logo" height="156">
  </a>
</div>



-----------------

## 介绍

支持中文拼写和语法错误纠正，并开源[拼写和语法错误的增强工具](https://github.com/TW-NLP/ChineseErrorCorrector/tree/0.1.0)、大模型训练代码、[文本纠错相关论文](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/README_paper.md)和[通用的文本纠错评测工具](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/ChineseErrorCorrector/scores/README.md)。荣获2024CCL 冠军
🏆， [2023 NLPCC-NaCGEC纠错冠军🏆](https://github.com/TW-NLP/ChineseErrorCorrector?tab=readme-ov-file#nacgec-%E6%95%B0%E6%8D%AE%E9%9B%86)， [2022 FCGEC 纠错冠军🏆](https://github.com/TW-NLP/ChineseErrorCorrector?tab=readme-ov-file#fcgec-%E6%95%B0%E6%8D%AE%E9%9B%86)
，如有帮助，感谢star✨。

## 🔥🔥🔥 新闻
[2026/02/28] 我们在 HuggingFace 和 ModelScope 开源了 ChineseErrorCorrector3 模型体验地址 🥳，欢迎大家访问进行试用。

  🤗 [HuggingFace 体验地址](https://huggingface.co/spaces/twnlp/ChineseErrorCorrector3) &nbsp;|&nbsp; 👉 [ModelScope 体验地址](https://www.modelscope.cn/studios/tiannlp/ChineseErrorCorrector)


[2025/12/11] 我们正在加速研发全新一代 ChineseErrorCorrector4 ⚡🔥，并同步筹备论文发布！这一版本将力求打造最强的中文文本纠错基线，提供更稳、更快、更准的整体体验。期待与大家再次相遇！🎉

[2025/11/25] 发布[ChineseErrorCorrector3-4B论文](https://arxiv.org/abs/2511.17562) 🎉，更多技术细节，欢迎大家查阅。

[2025/08/08] 发布[通用的文本评测工具-Common Errant（支持80种语言）](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/ChineseErrorCorrector/scores/README.md) 🎉，可以在高（中文、英文）、低资源（印地语、孟加拉语等）上进行文本纠错的评测。

[2025/08/06] 发布[文本纠错相关论文（持续更新版）](https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/README_paper.md) 🥳，方便大家进行研学。

[2025/08/01] 发布[twnlp/ChineseErrorCorrector3-4B](https://huggingface.co/twnlp/ChineseErrorCorrector3-4B) 🎉🎉🎉，泛化性全面提升，在开源的所有模型中，位列第一，[榜单详情](https://github.com/TW-NLP/ChineseErrorCorrector?tab=readme-ov-file#evaluation%E6%B3%9B%E5%8C%96%E6%80%A7%E8%AF%84%E6%B5%8B)。

[2025/05/01] 根据[建议](https://github.com/TW-NLP/ChineseErrorCorrector/issues/17)
，我们重新训练纠错模型(ChineseErrorCorrector2-7B)，并完全开源训练步骤，支持结果复现，[复现教程](https://github.com/TW-NLP/ChineseErrorCorrector/tree/v0.4.0?tab=readme-ov-file#%E5%AE%9E%E9%AA%8C%E7%BB%93%E6%9E%9C%E5%A4%8D%E7%8E%B0)

[2025/03/17]
更新批量错误文本的解析，[transformers批量解析](https://github.com/TW-NLP/ChineseErrorCorrector?tab=readme-ov-file#transformers-%E6%89%B9%E9%87%8F%E6%8E%A8%E7%90%86) ;[VLLM批量解析](https://github.com/TW-NLP/ChineseErrorCorrector?tab=readme-ov-file#vllm-%E5%BC%82%E6%AD%A5%E6%89%B9%E9%87%8F%E6%8E%A8%E7%90%86)

[2025/03/10] 模型支持多种推理方式，包括 transformers、VLLM、modelscope。

[2025/02/25]
🎉🎉🎉使用200万纠错数据进行多轮迭代训练，发布了[twnlp/ChineseErrorCorrector2-7B](https://huggingface.co/twnlp/ChineseErrorCorrector2-7B)
，在 [NaCGEC-2023NLPCC官方评测数据集](https://github.com/masr2000/NaCGEC)
上，超越第一名华为10个点，遥遥领先， [技术详情](https://blog.csdn.net/qq_43765734/article/details/145858955)

[2025/02]
为方便部署，使用38万开源拼写数据，发布了[twnlp/ChineseErrorCorrector-1.5B](https://huggingface.co/twnlp/ChineseErrorCorrector-1.5B)

[2025/01]
使用38万开源拼写数据，基于Qwen2.5训练中文拼写纠错模型，支持语似、形似等错误纠正，发布了[twnlp/ChineseErrorCorrector-7B](https://huggingface.co/twnlp/ChineseErrorCorrector-7B)，[twnlp/ChineseErrorCorrector-32B-LORA](https://huggingface.co/twnlp/ChineseErrorCorrector-32B-LORA/tree/main)

[2024/06]
v0.1.0版本：🎉🎉🎉开源一键语法错误增强工具，该工具可以进行14种语法错误的增强，不同行业可以根据自己的数据进行错误替换，来训练自己的语法和拼写模型。详见[Tag-v0.1.0](https://github.com/TW-NLP/ChineseErrorCorrector/tree/0.1.0)

## 🎯模型列表

| 模型名称                                                                                        | 纠错类型  | 描述                                         |
|:--------------------------------------------------------------------------------------------|:------|:-------------------------------------------|
| [twnlp/ChineseErrorCorrector3-4B](https://huggingface.co/twnlp/ChineseErrorCorrector3-4B)   | 语法+拼写 | 使用200万纠错数据进行全量训练，适用于语法纠错和拼写纠错，效果最好，推荐使用。   |
| [twnlp/ChineseErrorCorrector2-7B](https://huggingface.co/twnlp/ChineseErrorCorrector2-7B)   | 语法+拼写 | 使用200万纠错数据进行多轮迭代训练，适用于语法纠错和拼写纠错，效果较好。 |
| [twnlp/ChineseErrorCorrector-7B](https://huggingface.co/twnlp/ChineseErrorCorrector-7B)     | 拼写    | 使用38万开源拼写数据，支持语似、形似等拼写错误纠正，拼写纠错效果好。        |
| [twnlp/ChineseErrorCorrector-1.5B](https://huggingface.co/twnlp/ChineseErrorCorrector-1.5B) | 拼写    | 使用38万开源拼写数据，支持语似、形似等拼写错误纠正，拼写纠错效果一般。       |

## 📊数据集

| 数据集名称                        | 数据链接                                                                                             | 数据量和类别说明                                                                 | 描述                              |
|:-----------------------------|:-------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------|:--------------------------------|
| ChinseseErrorCorrectData     | [twnlp/ChinseseErrorCorrectData](https://huggingface.co/datasets/twnlp/ChinseseErrorCorrectData) | 200万                                                                     | ChineseErrorCorrector 训练数据集 |
| CSC（拼写纠错数据集）                 | [twnlp/csc_data](https://huggingface.co/datasets/twnlp/csc_data)                                 | W271K(279,816) Medical(39,303) Lemon(22,259) ECSpell(6,688) CSCD(35,001) | 中文拼写纠错的数据集                      |
| CGC（语法纠错数据集）                 | [twnlp/cgc_data](https://huggingface.co/datasets/twnlp/cgc_data)                                 | CGED(20,449) FCGEC(37,354) MuCGEC(2,467) NaCGEC(7,568)                   | 中文语法纠错的数据集                      |
| Lang8+HSK（百万语料-拼写和语法错误混合数据集） | [twnlp/lang8_hsk](https://huggingface.co/datasets/twnlp/lang8_hsk)                               | 1,568,885                                                                | 中文拼写和语法数据集                      |


##  🏗️ Evaluation


### 泛化性评测
- 评估指标：F1
- CSC(Chinese Spelling Correction): 拼写纠错模型，表示模型可以处理音似、形似、语法等长度对齐的错误纠正
- CTC(CHinese Text Correction): 文本纠错模型，表示模型支持拼写、语法等长度对齐的错误纠正，还可以处理多字、少字等长度不对齐的错误纠正
- GPU：Tesla V100，显存 32 GB

| Model Name        | Model Link                                                                                                              | Base Model                     | Avg        | SIGHAN-2015 | EC-LAW | MCSC   | GPU | QPS     |
|:------------------|:------------------------------------------------------------------------------------------------------------------------|:-------------------------------|:-----------|:------------|:-------|:-------|:--------|:--------|
| Kenlm-CSC         | [shibing624/chinese-kenlm-klm](https://huggingface.co/shibing624/chinese-kenlm-klm)                                     | kenlm                          | 0.3409     | 0.3147      | 0.3763 | 0.3317 | CPU     | 9       |
| Mengzi-T5-CSC     | [shibing624/mengzi-t5-base-chinese-correction](https://huggingface.co/shibing624/mengzi-t5-base-chinese-correction)     | mengzi-t5-base                 | 0.3984     | 0.7758      | 0.3156 | 0.1039 | GPU     | 214     |
| ERNIE-CSC         | [PaddleNLP/ernie-csc](https://github.com/PaddlePaddle/PaddleNLP/tree/develop/legacy/examples/text_correction/ernie-csc) | PaddlePaddle/ernie-1.0-base-zh | 0.4353     | 0.8383      | 0.3357 | 0.1318 | GPU     | 114     |
| MacBERT-CSC       | [shibing624/macbert4csc-base-chinese](https://huggingface.co/shibing624/macbert4csc-base-chinese)                       | hfl/chinese-macbert-base       | 0.3993     | 0.8314      | 0.1610 | 0.2055 | GPU     | **224** |
| ChatGLM3-6B-CSC   | [shibing624/chatglm3-6b-csc-chinese-lora](https://huggingface.co/shibing624/chatglm3-6b-csc-chinese-lora)               | THUDM/chatglm3-6b              | 0.4538     | 0.6572      | 0.4369 | 0.2672 | GPU     | 3       |
| Qwen2.5-1.5B-CTC  | [shibing624/chinese-text-correction-1.5b](https://huggingface.co/shibing624/chinese-text-correction-1.5b)               | Qwen/Qwen2.5-1.5B-Instruct     | 0.6802     | 0.3032      | 0.7846 | 0.9529 | GPU     | 6       |
| Qwen2.5-7B-CTC    | [shibing624/chinese-text-correction-7b](https://huggingface.co/shibing624/chinese-text-correction-7b)                   | Qwen/Qwen2.5-7B-Instruct       | 0.8225     | 0.4917      | 0.9798 | 0.9959 | GPU     | 3       |
| **Qwen3-4B-CTC(Our)** | [twnlp/ChineseErrorCorrector3-4B](https://huggingface.co/twnlp/ChineseErrorCorrector3-4B)                   | Qwen/Qwen3-4B                  | **0.8521** | 0.6340      | 0.9360 | 0.9864 | GPU     | 5       |

### 语法纠错(双冠军 🏆)

#### NaCGEC 数据集 🏆

- 评估工具：ChERRANT  [评测工具](https://github.com/HillZhang1999/MuCGEC)
- 评估数据：[NaCGEC](https://github.com/masr2000/NaCGEC)
- 评估指标：F1-0.5

| Model Name | Model Link | Prec | Rec | F0.5 |
|:-----------------|:---------------------------------------------------------------|:-----------|:------------|:-------|
| twnlp/ChineseErrorCorrector3-4B | [huggingface](https://huggingface.co/twnlp/ChineseErrorCorrector3-4B) ； [modelspose(国内下载)](https://www.modelscope.cn/models/tiannlp/ChineseErrorCorrector3-4B) | 0.542 | 0.3475 | 0.4874 |
| HW_TSC_nlpcc2023_cgec(华为) | 未开源 | 0.5095 | 0.3129 | 0.4526 |
| 鱼饼啾啾Plus(北京大学) | 未开源 | 0.5708 | 0.1294 | 0.3394 |
| CUHK_SU(香港中文大学) | 未开源 | 0.3882 | 0.1558 | 0.2990 |

####  FCGEC 数据集 🏆

- 评估指标：binary_f1

- [评测🔗](https://codalab.lisn.upsaclay.fr/competitions/8020#results)

## 🚀 快速开始
<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400">
</div>

### 🤗 transformers

```shell
pip install transformers
```

```shell
from transformers import AutoModelForCausalLM, AutoTokenizer,set_seed
set_seed(42)

model_name = "twnlp/ChineseErrorCorrector3-4B"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "你是一个文本纠错专家，纠正输入句子中的语法错误，并输出正确的句子，输入句子为："
text_input = "对待每一项工作都要一丝不够。"
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
print(response)

```

### VLLM

```shell
pip install transformers
pip install vllm==0.8.5
```

```shell
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained("twnlp/ChineseErrorCorrector3-4B")

# Pass the default decoding hyperparameters of twnlp/ChineseErrorCorrector3-4B
# max_tokens is for the maximum length for generation.
sampling_params = SamplingParams(seed=42,max_tokens=512)

# Input the model name or path. Can be GPTQ or AWQ models.
llm = LLM(model="twnlp/ChineseErrorCorrector3-4B")

# Prepare your prompts
text_input = "对待每一项工作都要一丝不够。"
messages = [
    {"role": "user", "content": "你是一个文本纠错专家，纠正输入句子中的语法错误，并输出正确的句子，输入句子为："+text_input}
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

### 👍 VLLM 异步批量推理(工程推荐)

- Clone the repo

``` sh
git clone https://github.com/TW-NLP/ChineseErrorCorrector
cd ChineseErrorCorrector
```

- Install Conda: please see https://docs.conda.io/en/latest/miniconda.html
- Create Conda env:

``` sh
conda create -n zh_correct -y python=3.10
conda activate zh_correct
pip install -r requirements.txt
# If you are in mainland China, you can set the mirror as follows:
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```
方法一：直接启动VLLM服务，使用openai接口进行调用，只输出正确语句，部署脚本：
``` sh
CUDA_VISIBLE_DEVICES=0 nohup vllm serve twnlp/ChineseErrorCorrector3-4B \
    --port 8000 \
    --max-model-len 1024 \
    --gpu-memory-utilization 0.9 \
    --seed 42 \
    >chinese_corrector.log 2>&1 &
```
cURL 调用（openai格式）
``` sh
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "twnlp/ChineseErrorCorrector3-4B",
    "messages": [
      {
        "role": "user",
        "content": "你是一个文本纠错专家，纠正输入句子中的语法错误，并输出正确的句子，输入句子为：对待每一项工作都要一丝不够。"
      }
    ],
    "max_tokens": 1024,
    "temperature": 0,
    "seed": 42
  }'
```

方法二：使用ChineseErrorCorrector推理，有对应的后处理操作。
```sh
# 修改config.py
#（1）根据不同的模型，修改的DEFAULT_CKPT_PATH，默认为twnlp/ChineseErrorCorrector3-4B(将模型下载，放在ChineseErrorCorrector/pre_model/twnlp/ChineseErrorCorrector3-4B)
#（2）将TextCorrectConfig的USE_VLLM = True

#批量预测
python main.py
#输出：
'''
[{'source': '对待每一项工作都要一丝不够。', 'target': '对待每一项工作都要一丝不苟。', 'errors': [('够', '苟', 12)]}, {'source': '大约半个小时左右', 'target': '大约半个小时', 'errors': [('左右', '', 6)]}]
'''
```


### Transformers 批量推理

- Clone the repo

``` sh
git clone https://github.com/TW-NLP/ChineseErrorCorrector
cd ChineseErrorCorrector
```

- Install Conda: please see https://docs.conda.io/en/latest/miniconda.html
- Create Conda env:

``` sh
conda create -n zh_correct -y python=3.10
conda activate zh_correct
pip install -r requirements.txt
# If you are in mainland China, you can set the mirror as follows:
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

``` sh
# 修改config.py
#（1）根据不同的模型，修改的DEFAULT_CKPT_PATH，默认为twnlp/ChineseErrorCorrector3-4B
#（2）将TextCorrectConfig的USE_VLLM = False

#批量预测
python main.py

```

### 🤖 modelscope

```shell
pip install modelscope
```

```shell
from modelscope import AutoModelForCausalLM, AutoTokenizer

model_name = "tiannlp/twnlp/ChineseErrorCorrector3-4B"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "你是一个文本纠错专家，纠正输入句子中的语法错误，并输出正确的句子，输入句子为："
text_input = "对待每一项工作都要一丝不够。"
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
print(response)

```


## Citation

If this work is helpful, please kindly cite as:

```bibtex

@misc{tian2025chineseerrorcorrector34bstateoftheartchinesespelling,
      title={ChineseErrorCorrector3-4B: State-of-the-Art Chinese Spelling and Grammar Corrector}, 
      author={Wei Tian and YuhaoZhou},
      year={2025},
      eprint={2511.17562},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2511.17562}, 
}
```
## Contact

**微信：** NLP技术交流群。

<img src="https://github.com/TW-NLP/ChineseErrorCorrector/blob/main/images/chat.jpg" width="200" />


## References

* [中文纠错系统](https://github.com/shibing624/pycorrector)
* [纠错论文](https://github.com/nghuyong/Chinese-text-correction-papers)
* [纠错评测](https://github.com/open-writing-evaluation/jp_errant_bea)
