import os
import torch

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(PROJECT_DIR, 'pre_model')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE_COUNT = 1 if torch.cuda.device_count() == 1 else int(torch.cuda.device_count() // 2) * 2


class LTPPath(object):
    LTP_MODEL_DIR = os.path.join(MODEL_DIR, 'ltp_tiny')
    LTP_DATA_PATH = os.path.join(DATA_DIR, 'dat_data')


class StanzaPath(object):
    STANZA_DATA_PATH = os.path.join(DATA_DIR, 'stanza', 'stanza_resources_1.7.0.json')


class TextCorrectConfig(object):
    """
    纠错主链路：通过 OpenAI 兼容接口调用部署好的 4B 大模型（例如本地 vLLM serve）。
    本仓库的推理代码不再直接加载 4B 大模型权重，所有生成请求都走 HTTP / OpenAI SDK。
    """

    # ---- 4B 大模型 OpenAI 接口（必选） ----
    # vLLM serve 默认即为 OpenAI 兼容接口，可配合 README 中给出的部署脚本使用。
    OPENAI_BASE_URL = os.environ.get("CEC_OPENAI_BASE_URL", "http://localhost:8000/v1")
    OPENAI_API_KEY = os.environ.get("CEC_OPENAI_API_KEY", "EMPTY")
    OPENAI_MODEL = os.environ.get("CEC_OPENAI_MODEL", "twnlp/ChineseErrorCorrector3-4B")

    # 生成参数
    MAX_TOKENS = 1024
    TEMPERATURE = 0
    SEED = 42
    # 并发请求数（异步批量推理时使用）
    CONCURRENCY = 16
    # 单次请求超时（秒）
    REQUEST_TIMEOUT = 60

    # ---- ELECTRA 字级门控（可选，默认关闭） ----
    # 启用后，会先用轻量 ELECTRA 判别器筛掉「明显无错」的句子，仅对需要纠错的句子调用大模型。
    # 详细说明见 README_ELECTRA.md。
    #
    # 模型下载与放置（推荐）：
    #   1) 从 https://huggingface.co/xurong123/ChineseErrorDetectorElectra 下载权重
    #   2) 放到 ChineseErrorCorrector/pre_model/ChineseErrorDetectorElectra/ 下（即下方默认路径）
    #   3) 也可设置环境变量 CHAR_GATE_HF_REPO_ID 覆盖，或直接填 HF 仓库 id 走在线加载
    USE_DETECTOR = False
    DEFAULT_DETECTOR_PATH = os.environ.get(
        "CHAR_GATE_HF_REPO_ID",
        os.path.join(MODEL_DIR, "ChineseErrorDetectorElectra"),
    )
    DETECTOR_SENTENCE_THRESHOLD = 0.5
    DETECTOR_MAX_LENGTH = 256
    DETECTOR_BATCH_SIZE = 32


class TrainConfig(object):
    """
    模型数据与模型保存
    """
    TRAIN_PATH = os.path.join(DATA_DIR, 'business_data', 'train.json')
    DEV_PATH = os.path.join(DATA_DIR, 'business_data', 'valid.json')
    SAVE_PATH = os.path.join(DATA_DIR, 'business_data', 'model_output')
    CACHE_PATH = os.path.join(DATA_DIR, 'cache')
