# -*- coding:utf-8 -*-
"""下载 bge-small-zh-v1.5 句向量模型到项目根目录。

该模型用于 RAG 案例检索的文本向量化。下载后会保存到项目根目录的
``bge-small-zh-v1.5/`` 目录（已在 .gitignore 中忽略），后端 config
会自动拼接绝对路径加载。

用法::

    python scripts/download_bge_model.py
"""
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from transformers import AutoModel, AutoTokenizer

model_name = "BAAI/bge-small-zh-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

save_path = "./bge-small-zh-v1.5"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

if __name__ == "__main__":
    print(f"模型已保存到 {save_path}")
