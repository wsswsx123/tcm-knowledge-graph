# backend/app/services/agents/symptom_agent.py
"""一级 Agent：用户情况提取。

新定位（2026-10 重构）：
体质由王琦量表问卷锁定，本 Agent 不再用于"辨证"，只负责从用户闲聊里提取两类信息：

1. symptoms：用户提到的主观不适（保留原字段，供漂移检测对比 locked 体质用）。
2. constraints：个性化约束（新增），供 PlanRefiner 在已有方案上做裁剪：
   - contraindications：禁忌（慢病、孕哺、过敏、术后、急性病）
   - preferences：生活偏好（不吃辣/素食/上班族久坐/怕累/没场地）
   - current_state：当前临时状态（感冒、经期、熬夜、膝盖疼、出差）
"""
import logging
import re
from typing import Any, Dict, List

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


# ---------- 个性化约束的关键词规则表 ----------

# (关键词列表, 类别, 标签, 对方案的影响方向)
# 影响方向：
#   avoid_warm   → 暂停温补类食材（羊肉、桂圆、红枣）
#   avoid_cold   → 暂停寒凉类食材（绿豆、苦瓜、西瓜）
#   avoid_strenuous → 暂停高强度运动（跑步、爬山、球类），换成散步/八段锦
#   avoid_acupoint_abdomen → 暂停腹部/腰骶穴位（孕期）
#   soft_diet    → 推荐温软食物，暂停生冷辛辣
#   reduce_exercise → 运动减量
_CONSTRAINT_RULES = [
    # —— 急性病/外感 ——
    (['感冒', '着凉', '发烧', '发热', '咳嗽', '喉咙痛', '嗓子疼'],
     'current_state', '感冒/外感期间', 'avoid_warm'),
    (['拉肚子', '腹泻', '肠胃炎', '胃痛', '胃不舒服', '胃寒'],
     'current_state', '肠胃不适', 'soft_diet'),
    # —— 女性特殊时期 ——
    (['怀孕', '孕期', '备孕', '哺乳期', '喂奶'],
     'contraindications', '孕哺期', 'avoid_acupoint_abdomen'),
    (['经期', '姨妈', '月经来了', '痛经'],
     'current_state', '经期', 'avoid_cold'),
    # —— 运动相关约束 ——
    (['膝盖不好', '膝盖疼', '膝关节', '腰突', '腰椎', '腰不好', '腰伤',
      '腿不好', '脚崴', '脚踝', '关节炎', '半月板'],
     'contraindications', '下肢关节损伤', 'avoid_strenuous'),
    (['高血压', '血压高', '心脏病', '冠心病', '心梗', '中风'],
     'contraindications', '心脑血管问题', 'reduce_exercise'),
    (['上班族', '久坐', '加班', '996', '没时间', '懒人', '怕累', '懒得动'],
     'preferences', '久坐忙碌/怕累', 'reduce_exercise'),
    # —— 饮食偏好 ——
    (['不吃辣', '怕辣', '不能吃辣', '忌口辛辣'],
     'preferences', '忌辛辣', 'avoid_spicy'),
    (['素食', '吃素', '不吃肉', '不喜欢吃肉'],
     'preferences', '素食倾向', 'prefer_vegetarian'),
    (['脾胃虚', '消化不好', '容易拉肚子', '怕吃凉'],
     'contraindications', '脾胃虚寒', 'avoid_cold'),
    # —— 过敏/特禀 ——
    (['过敏', '对xx过敏', '花粉症', '过敏性鼻炎', '哮喘'],
     'contraindications', '过敏体质', 'avoid_pollen_exercise'),
]


class SymptomAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='symptom_agent', role='用户情况提取')

    def analyze(self, user_input: str, trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        输入：用户原始对话文本。
        输出：{
          symptoms: [...],            # 提到的不适（漂移检测用）
          tongue: str, pulse: str,    # 保留兼容字段（新定位下基本不用）
          completeness: str,
          constraints: {             # 新增：个性化约束
            contraindications: [{'label': str, 'impact': str}],
            preferences: [...],
            current_state: [...],
          }
        }
        """
        # 规则提取（零延迟，主路径）
        result = self._extract_rules(user_input)
        trace.append({
            'agent': self.name, 'note': '规则提取用户情况',
            'constraints_count': sum(len(v) for v in result['constraints'].values()),
        })
        return result

    def _extract_rules(self, user_input: str) -> Dict[str, Any]:
        text = user_input or ''
        # 1) 提取症状关键词（保留兼容，用于漂移检测）
        symptom_keywords = [
            '疲乏', '乏力', '倦怠', '气短', '懒言', '自汗', '易出汗',
            '畏寒', '怕冷', '手足不温', '手脚凉', '手脚心热',
            '五心烦热', '盗汗', '口燥咽干', '口干', '口苦', '潮热',
            '胸闷', '脘腹痞闷', '痰多', '口中黏腻', '口黏',
            '面垢油光', '面部出油', '痤疮', '身重困倦', '头身困重',
            '大便黏', '大便干', '小便黄', '心烦', '烦躁',
            '皮肤晦暗', '色素沉着',
            '情绪低落', '善太息', '爱叹气', '胸胁胀满',
            '失眠', '睡眠差', '入睡困难', '多梦',
            '过敏', '皮疹', '喷嚏',
        ]
        symptoms: List[str] = []
        for k in symptom_keywords:
            idx = text.find(k)
            if idx < 0:
                continue
            window = text[max(0, idx - 6):idx]
            if any(neg in window for neg in ('不', '没', '无')):
                continue
            symptoms.append(k)

        # 2) 提取个性化约束
        constraints = {
            'contraindications': [],
            'preferences': [],
            'current_state': [],
        }
        seen_labels = set()
        for keywords, category, label, impact in _CONSTRAINT_RULES:
            if any(k in text for k in keywords):
                if label in seen_labels:
                    continue
                seen_labels.add(label)
                constraints[category].append({'label': label, 'impact': impact})

        completeness = '部分' if symptoms else '无不适'

        return {
            'symptoms': symptoms if symptoms else ['信息不足'],
            'tongue': '未采集',
            'pulse': '未采集',
            'completeness': completeness,
            'constraints': constraints,
        }
