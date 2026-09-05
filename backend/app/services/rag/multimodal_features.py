# backend/app/services/rag/multimodal_features.py
"""
多模态特征模拟：舌象/脉象文本特征化。

说明：项目暂不引入真实图像/波形数据。这里把舌象、脉象描述文本与症状文本拼接，
统一通过 embedding 向量化后送入向量库召回——形成"多模态特征融合"的文本模拟链路。
接口预留 encode_tongue/encode_pulse，便于后续替换为真实图像/波形编码器。
"""
from typing import List


def build_case_text(symptoms: List[str], tongue: str = "", pulse: str = "",
                    syndrome: str = "") -> str:
    """将案例的各模态文本拼接为统一检索文本。"""
    parts = []
    if symptoms:
        parts.append("症状：" + "；".join(symptoms))
    if tongue:
        parts.append("舌象：" + tongue)
    if pulse:
        parts.append("脉象：" + pulse)
    if syndrome:
        parts.append("证型：" + syndrome)
    return "。".join(parts)


def build_query_text(symptoms: List[str], tongue: str = "", pulse: str = "") -> str:
    """将用户查询的各模态文本拼接为统一检索文本。"""
    return build_case_text(symptoms, tongue=tongue, pulse=pulse, syndrome="")


def encode_tongue(tongue_text: str) -> str:
    """
    预留：舌象特征编码。当前返回归一化文本，后续可替换为图像编码器输出。
    """
    if not tongue_text:
        return ""
    return tongue_text.replace("舌", "").strip()


def encode_pulse(pulse_text: str) -> str:
    """
    预留：脉象特征编码。当前返回归一化文本，后续可替换为波形编码器输出。
    """
    if not pulse_text:
        return ""
    return pulse_text.replace("脉", "").strip()
