# -*- coding:utf-8 -*-
# @Author: 喵酱
# @time: 2025 - 04 -05
# @File: miao_test.py
# desc:
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from transformers import AutoModel, AutoTokenizer

model_name = "BAAI/bge-small-zh-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# 保存模型到本地目录（例如 ./bge-small-zh-v1.5）
save_path = "./bge-small-zh-v1.5"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
if __name__ == '__main__':
    print(f"模型已保存到 {save_path}")
