# backend/app/services/ai_service.py
"""
AI服务模块，支持多模型（千问 / 仲景）
"""
import json
import re
import logging
import time
from typing import Dict, List, Optional, Union

from ..config import Config
from .model_loader import load_model, unload_model

logger = logging.getLogger(__name__)


class QwenTCMService:
    """通用中医AI服务，支持动态选择模型"""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or getattr(Config, 'DEFAULT_MODEL', 'qwen')
        self.use_ollama = getattr(Config, 'USE_OLLAMA', False)
        self.ollama_url = getattr(Config, 'OLLAMA_URL', 'http://localhost:11434/api/generate')

        if self.use_ollama:
            self.model = None
            self.tokenizer = None
            logger.info("使用 Ollama 后端")
        else:
            logger.info(f"正在加载本地模型: {self.model_name}")
            self.model, self.tokenizer = load_model(self.model_name)
            if self.model is None:
                logger.error(f"模型 {self.model_name} 加载失败")
            else:
                logger.info(f"模型 {self.model_name} 加载成功")

        # 任务提示模板
        self.system_prompts = {
            "explain": "你是一位亲切的中医助手，用通俗易懂的语言解释问卷问题。回答要简短（50字内），包含生活化例子。",
            "followup": "你是一位专业的中医体质辨识专家，根据已答问题生成有针对性的追问。",
            "interpret": "你是一位温暖的中医体质解读专家，用鼓励的语气解读用户的体质测评结果。",
            "recommend": "你是一位经验丰富的中医养生专家，基于体质推荐个性化的调理方案。",
            "wellness_plan": """你是一位资深的中医养生专家，擅长根据体质制定个性化的养生计划。请根据用户体质，生成包含饮食宜忌、推荐食谱、运动建议、情志调理和作息建议的详细周计划。回答应专业、实用、温暖，使用清晰的Markdown格式。"""
        }

    def _build_prompt(self, task: str, user_input: str, context: Optional[Dict] = None) -> str:
        system = self.system_prompts.get(task, "你是一个专业的中医助手。")
        context_str = ""
        if context:
            if task == "explain":
                context_str = f"问题：{context.get('question', '')}\n体质类型：{context.get('constitution', '')}\n"
            elif task == "followup":
                context_str = f"已答问题：{json.dumps(context.get('answers', []), ensure_ascii=False)}\n当前分数：{json.dumps(context.get('scores', {}), ensure_ascii=False)}\n"
            elif task == "interpret":
                context_str = f"主体质：{context.get('primary', '')}\n兼夹体质：{', '.join(context.get('secondary', []))}\n各体质分数：{json.dumps(context.get('scores', {}), ensure_ascii=False)}\n"
            elif task == "recommend":
                context_str = f"主体质：{context.get('primary', '')}\n兼夹体质：{', '.join(context.get('secondary', []))}\n图谱推荐：{json.dumps(context.get('base_recs', {}), ensure_ascii=False)}\n"
        messages = [{"role": "system", "content": system}, {"role": "user", "content": f"{context_str}{user_input}"}]
        if self.tokenizer:
            prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        else:
            prompt = f"<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{context_str}{user_input}<|im_end|>\n<|im_start|>assistant\n"
        return prompt

    def _generate_ollama(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        import requests
        # 模型名统一读配置（OLLAMA_MODEL），不再硬编码——换模型只需改 .env
        ollama_models = getattr(Config, 'OLLAMA_MODEL_MAP', None) or {
            'qwen': getattr(Config, 'OLLAMA_MODEL', 'qwen2.5:3b')}
        model = ollama_models.get(self.model_name) or getattr(Config, 'OLLAMA_MODEL', 'qwen2.5:3b')
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"max_tokens": max_tokens, "temperature": temperature, "top_p": 0.9}
        }
        try:
            resp = requests.post(self.ollama_url, json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as e:
            logger.error(f"Ollama请求失败: {e}")
            return "【服务暂时不可用】"

    def _generate_transformers(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        if self.model is None or self.tokenizer is None:
            return "【模型未加载】"
        try:
            import torch
        except Exception as e:
            logger.error(f"torch 不可用，无法走本地 transformers 推理: {e}")
            return "【本地模型不可用，请改用 Ollama 后端】"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
        response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        return response.strip()

    def generate(self, task: str, user_input: str, context: Optional[Dict] = None,
                 max_tokens: int = 256, temperature: float = 0.7) -> str:
        prompt = self._build_prompt(task, user_input, context)
        if self.use_ollama:
            return self._generate_ollama(prompt, max_tokens, temperature)
        else:
            return self._generate_transformers(prompt, max_tokens, temperature)

    def generate_structured(self, task: str, user_input: str, context: Optional[Dict] = None,
                            max_tokens: int = 512, temperature: float = 0.3) -> Dict:
        response = self.generate(task, user_input, context, max_tokens, temperature)
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"error": "无法解析JSON", "raw": response}
        except Exception as e:
            logger.error(f"JSON解析失败: {e}")
            return {"error": str(e), "raw": response}

    def explain_question(self, question: Dict) -> str:
        context = {"question": question['content'], "constitution": question.get('constitution_name', '')}
        user_input = "请用通俗语言解释这个问题，并举一个生活例子。"
        return self.generate("explain", user_input, context, max_tokens=100)

    def generate_followup(self, answers: List[Dict], scores: Dict, uncertain_types: List[str]) -> List[str]:
        if not uncertain_types:
            return []
        answers_desc = "\n".join([f"问题：{a.get('question', '')} 答案：{a.get('value', 0)}分" for a in answers[-5:]])
        scores_desc = "\n".join([f"{t}: {s}分" for t, s in scores.items() if t in uncertain_types])
        prompt = f"""
你是一位专业的中医体质辨识专家。用户正在填写体质问卷，目前有以下体质得分处于临界范围（30-39分），需要进一步确认：
临界体质得分：
{scores_desc}
最近回答的问题：
{answers_desc}
请针对这些临界体质生成1-2个追问问题，每个问题应该是5级评分（1-5分），选项为：1=没有，2=很少，3=有时，4=经常，5=总是
要求：
1. 问题要针对该体质的典型症状
2. 问题表述符合中医体质问卷的风格
3. 返回严格的JSON数组格式，例如：["问题1", "问题2"]
只返回JSON数组，不要有其他文字。
"""
        for attempt in range(3):
            result = self.generate_structured("followup", prompt, max_tokens=300, temperature=0.2)
            if isinstance(result, list) and result:
                return result
            if isinstance(result, dict) and 'raw' in result:
                raw = result['raw'].strip()
                # 移除 markdown 标记
                if raw.startswith('```json'):
                    raw = raw[7:]
                if raw.startswith('```'):
                    raw = raw[3:]
                if raw.endswith('```'):
                    raw = raw[:-3]
                raw = raw.strip()
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        return parsed
                except json.JSONDecodeError:
                    match = re.search(r'\[.*\]', raw, re.DOTALL)
                    if match:
                        try:
                            parsed = json.loads(match.group())
                            if isinstance(parsed, list):
                                return parsed
                        except:
                            pass
            if attempt < 2:
                time.sleep(0.5)
        logger.warning(f"追问生成失败，返回空列表。原始输出: {result}")
        return []

    def interpret_result(self, result: Dict) -> str:
        context = {
            "primary": result['primary_name'],
            "secondary": result.get('secondary_names', []),
            "scores": result['scores']
        }
        user_input = "请用温暖鼓励的语气解读这个体质测评结果，强调这是可以通过调理改善的。"
        return self.generate("interpret", user_input, context, max_tokens=300)

    def enhance_recommendations(self, result: Dict, base_recs: Dict) -> Dict:
        if not base_recs or (not base_recs.get('acupoints') and not base_recs.get('foods') and not base_recs.get('exercises')):
            return base_recs
        context = {
            "primary": result['primary_name'],
            "secondary": result.get('secondary_names', []),
            "base_recs": base_recs
        }
        user_input = """
请从基础推荐中精选3-5项，为每项生成个性化说明。
返回严格的JSON格式，每个项目必须包含原有的属性，并添加reason字段：
{
    "acupoints": [{"name": "足三里", "location": "...", "method": "...", "reason": "..."}],
    "foods": [{"name": "山药", "nature": "平", "effect": "...", "reason": "..."}],
    "exercises": [{"name": "八段锦", "effect": "...", "method": "...", "reason": "..."}],
    "precautions": ["..."]
}
注意：每个项目必须包含原基础推荐中的所有字段，并额外添加reason字段。
"""
        ai_out = self.generate_structured("recommend", user_input, context)
        # 防御性兜底：AI 输出异常（无法解析 JSON）时，generate_structured 会返回
        # {"error": "...", "raw": "..."}。此时必须回落到原始 base_recs（同时保留 precautions 为空），
        # 否则调用方按数组访问 .acupoints/.foods/.exercises 全部为 undefined。
        if (
            isinstance(ai_out, dict)
            and (
                isinstance(ai_out.get('acupoints'), list)
                or isinstance(ai_out.get('foods'), list)
                or isinstance(ai_out.get('exercises'), list)
            )
        ):
            # 合并：AI 没返回的字段直接保留 base_recs 的结果，避免丢数据
            merged = dict(base_recs)
            for key in ('acupoints', 'foods', 'exercises', 'precautions',
                        'therapy_process', 'health_knowledge'):
                if isinstance(ai_out.get(key), list) and len(ai_out[key]) > 0:
                    merged[key] = ai_out[key]
                elif key not in merged:
                    merged[key] = ai_out.get(key, []) if isinstance(ai_out.get(key), list) else []
            # precautions 合并：AI 生成的优先，其次保留图谱
            if 'precautions' in ai_out and isinstance(ai_out['precautions'], list):
                merged['precautions'] = ai_out['precautions'] or merged.get('precautions', [])
            return merged
        logger.warning(
            "enhance_recommendations: AI 输出异常，回落到基础推荐。原始输出: %s",
            ai_out,
        )
        return dict(base_recs)

    def unload(self):
        if not self.use_ollama:
            unload_model(self.model_name)
            self.model = None
            self.tokenizer = None
            logger.info(f"模型 {self.model_name} 已卸载")


_service_instances = {}

def get_ai_service(model_name: str = None) -> QwenTCMService:
    if model_name is None:
        model_name = getattr(Config, 'DEFAULT_MODEL', 'qwen')
    if model_name not in _service_instances:
        _service_instances[model_name] = QwenTCMService(model_name)
    return _service_instances[model_name]