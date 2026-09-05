# backend/app/services/model_loader.py
import os
import logging
import importlib

logger = logging.getLogger(__name__)

_model_instances = {}
_tokenizer_instances = {}

def is_bitsandbytes_available():
    try:
        importlib.metadata.version("bitsandbytes")
        import bitsandbytes
        return True
    except (importlib.metadata.PackageNotFoundError, ImportError):
        return False

def load_model(model_name: str, use_4bit: bool = True):
    """加载本地 transformers 模型。torch/transformers 延迟导入，Ollama 模式下不触发。"""
    global _model_instances, _tokenizer_instances

    if model_name in _model_instances:
        logger.info(f"模型 {model_name} 已存在，直接返回")
        return _model_instances[model_name], _tokenizer_instances[model_name]

    logger.info(f"正在加载模型: {model_name}")

    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    except Exception as e:
        logger.error(f"torch/transformers 不可用，无法加载本地模型: {e}")
        return None, None

    from ..config import Config

    # GPU 检测
    gpu_available = torch.cuda.is_available()
    if gpu_available:
        total_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        logger.info(f"检测到 GPU，显存总量: {total_vram:.2f} GB")
        if total_vram < 4.0:
            logger.warning(f"GPU 显存不足 ({total_vram:.2f} GB < 4GB)，将使用 CPU 加载模型")
            gpu_available = False
    else:
        logger.info("未检测到 GPU，将使用 CPU")

    bnb_available = is_bitsandbytes_available()
    if use_4bit and not bnb_available:
        logger.warning("bitsandbytes 未安装或不可用，将不使用 4bit 量化")
        use_4bit = False

    # 量化配置
    if use_4bit and gpu_available and bnb_available:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        device_map = "auto"
        torch_dtype = torch.float16
        logger.info("使用 4bit 量化 + GPU 模式")
    elif use_4bit and not gpu_available and bnb_available:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float32,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        device_map = "cpu"
        torch_dtype = torch.float32
        logger.info("使用 4bit 量化 + CPU 模式")
    else:
        quantization_config = None
        device_map = "auto" if gpu_available else "cpu"
        torch_dtype = torch.float16 if gpu_available else torch.float32
        logger.info("未使用量化")

    try:
        if model_name == 'qwen':
            model_path = Config.MODEL_PATH_QWEN
            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=quantization_config,
                device_map=device_map,
                torch_dtype=torch_dtype,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
        elif model_name == 'zhongjing':
            model_path = Config.MODEL_PATH_ZHONGJING
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"仲景模型路径不存在: {model_path}")
            # 修复 config.json 中的 quantization_config 问题
            import json
            config_file = os.path.join(model_path, "config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                if "quantization_config" in cfg:
                    del cfg["quantization_config"]
                    with open(config_file, 'w', encoding='utf-8') as f:
                        json.dump(cfg, f, indent=2)
                    logger.info("已删除仲景模型 config.json 中的 quantization_config 字段")
            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=quantization_config,
                device_map=device_map,
                torch_dtype=torch_dtype,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
        else:
            raise ValueError(f"不支持的模型名称: {model_name}")

        model.eval()
        _model_instances[model_name] = model
        _tokenizer_instances[model_name] = tokenizer
        logger.info(f"模型 {model_name} 加载成功，设备映射: {model.device if hasattr(model, 'device') else device_map}")
        return model, tokenizer

    except Exception as e:
        logger.error(f"模型加载失败 ({model_name}): {e}")
        # 如果 GPU 模式失败，尝试 CPU 模式
        if gpu_available:
            logger.warning("GPU 模式失败，尝试使用 CPU 模式重新加载...")
            return _load_model_cpu_fallback(model_name)
        else:
            return None, None

def _load_model_cpu_fallback(model_name: str):
    logger.info(f"尝试以 CPU 模式加载模型 {model_name}")
    from ..config import Config
    try:
        quantization_config = None
        device_map = "cpu"
        torch_dtype = torch.float32
        if model_name == 'qwen':
            model_path = Config.MODEL_PATH_QWEN
            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=quantization_config,
                device_map=device_map,
                torch_dtype=torch_dtype,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
        elif model_name == 'zhongjing':
            model_path = Config.MODEL_PATH_ZHONGJING
            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=quantization_config,
                device_map=device_map,
                torch_dtype=torch_dtype,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
        else:
            raise ValueError(f"不支持的模型名称: {model_name}")
        model.eval()
        _model_instances[model_name] = model
        _tokenizer_instances[model_name] = tokenizer
        logger.info(f"CPU 模式加载模型 {model_name} 成功")
        return model, tokenizer
    except Exception as e:
        logger.error(f"CPU 模式加载也失败: {e}")
        return None, None

def unload_model(model_name: str = None):
    global _model_instances, _tokenizer_instances
    if model_name:
        _model_instances.pop(model_name, None)
        _tokenizer_instances.pop(model_name, None)
    else:
        _model_instances.clear()
        _tokenizer_instances.clear()
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass
    logger.info(f"模型已卸载: {model_name if model_name else 'all'}")