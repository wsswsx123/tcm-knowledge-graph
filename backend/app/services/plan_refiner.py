# backend/app/services/plan_refiner.py
"""
方案裁剪器：基于用户的个性化约束，对已生成的调理方案做个性化筛选。

输入：
  - 原始方案 plan（来自 checkpoints.plan.plan_result.plan）
  - constraints（来自 SymptomAgent：{contraindications, preferences, current_state}）

输出：每项加 status 字段：
  - keep    保留推荐
  - pause   暂时不适合（说明原因）
  - replace 不适合 + 给替代建议

纯规则实现，不调 LLM，零延迟。
"""
from typing import Any, Dict, List


# 性味偏温的食材关键词（感冒/外感期间暂停温补）
_WARM_FOOD_KEYWORDS = ['羊肉', '牛肉', '桂圆', '龙眼', '荔枝', '红枣', '大枣',
                       '姜', '肉桂', '花椒', '八角', '榴莲', '樱桃']
# 性味偏凉的食材关键词（经期/脾胃虚寒暂停）
_COLD_FOOD_KEYWORDS = ['绿豆', '苦瓜', '西瓜', '梨', '螃蟹', '海带', '紫菜',
                       '冰淇淋', '冷饮', '凉茶', '猕猴桃', '柚子', '荸荠']
# 高冲击运动关键词（关节损伤/心脑血管暂停）
_STRENUOUS_EXERCISE_KEYWORDS = ['跑步', '快跑', '爬山', '登山', '球类', '篮球',
                                '足球', '羽毛球', '网球', '跳绳', '深蹲', '马拉松']
# 腹部/腰骶穴位（孕期暂停）
_ABDOMEN_ACUPOINT_KEYWORDS = ['关元', '气海', '中脘', '神阙', '天枢', '子宫',
                              '八髎', '肾俞', '命门', '腰阳关']


def refine_plan(plan: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
    """
    返回裁剪后的方案结构（原地深拷贝修改）：
    {
      acupoints: [{..., status, pause_reason?, replacement?}],
      foods:     [...],
      exercises: [...],
      precautions: [...],
      summary:   {'paused_count': int, 'replaced_count': int, 'notes': [str]}
    }
    """
    if not isinstance(plan, dict):
        return plan or {}

    contra = list((constraints or {}).get('contraindications') or [])
    pref = list((constraints or {}).get('preferences') or [])
    state = list((constraints or {}).get('current_state') or [])
    all_impacts = set()
    for c in contra + pref + state:
        imp = c.get('impact')
        if imp:
            all_impacts.add(imp)

    notes: List[str] = []
    paused_count = 0
    replaced_count = 0

    # —— 裁剪食材 ——
    foods_out = []
    for f in (plan.get('foods') or []):
        item = dict(f)
        name = str(f.get('name', ''))
        nature = str(f.get('nature', ''))
        item['status'] = 'keep'

        if 'avoid_warm' in all_impacts and _hit_any(name + nature, _WARM_FOOD_KEYWORDS):
            item['status'] = 'pause'
            item['pause_reason'] = '你提到正在感冒/外感期间，温补食材容易把邪门关住，先暂时停一停'
            paused_count += 1
        elif 'avoid_cold' in all_impacts and _hit_any(name + nature, _COLD_FOOD_KEYWORDS):
            item['status'] = 'pause'
            item['pause_reason'] = '你提到经期/脾胃偏虚，寒凉食物先放一放，免得不舒服'
            paused_count += 1
        elif 'avoid_spicy' in all_impacts and ('辣' in name or '椒' in name):
            item['status'] = 'pause'
            item['pause_reason'] = '你说忌口辛辣，这个先不推荐啦'
            paused_count += 1
        elif 'prefer_vegetarian' in all_impacts and _is_animal_food(name):
            item['status'] = 'pause'
            item['pause_reason'] = '你是素食倾向，这个荤食先跳过'
            paused_count += 1
        foods_out.append(item)

    # —— 裁剪运动 ——
    exercises_out = []
    for e in (plan.get('exercises') or []):
        item = dict(e)
        name = str(e.get('name', ''))
        method = str(e.get('method', ''))
        item['status'] = 'keep'

        if 'avoid_strenuous' in all_impacts and _hit_any(name + method, _STRENUOUS_EXERCISE_KEYWORDS):
            item['status'] = 'replace'
            item['pause_reason'] = '你说关节不太好，这种对膝盖/腰椎冲击大的运动先别做'
            item['replacement'] = '换成八段锦、慢走、太极这类温和的，关节压力小'
            replaced_count += 1
        elif 'reduce_exercise' in all_impacts and _hit_any(name + method, _STRENUOUS_EXERCISE_KEYWORDS):
            item['status'] = 'pause'
            item['pause_reason'] = '你提到心脑血管/忙碌怕累，这类运动先减量或换成慢走'
            paused_count += 1
        elif 'avoid_pollen_exercise' in all_impacts and any(k in name + method for k in ('户外', '公园', '登山')):
            item['status'] = 'pause'
            item['pause_reason'] = '你有过敏倾向，户外花粉季先改室内运动'
            paused_count += 1
        exercises_out.append(item)

    # —— 裁剪穴位 ——
    acupoints_out = []
    for a in (plan.get('acupoints') or []):
        item = dict(a)
        name = str(a.get('name', ''))
        item['status'] = 'keep'
        if 'avoid_acupoint_abdomen' in all_impacts and _hit_any(name, _ABDOMEN_ACUPOINT_KEYWORDS):
            item['status'] = 'pause'
            item['pause_reason'] = '孕哺期腹部/腰骶穴位先别按，安全第一'
            paused_count += 1
        acupoints_out.append(item)

    # —— 备注 ——
    if paused_count:
        notes.append(f'根据你说的情况，我帮你把 {paused_count} 项暂时标为"不建议"')
    if replaced_count:
        notes.append(f'{replaced_count} 项运动给你换了更温和的替代')

    return {
        'acupoints': acupoints_out,
        'foods': foods_out,
        'exercises': exercises_out,
        'precautions': plan.get('precautions') or [],
        'summary': {
            'paused_count': paused_count,
            'replaced_count': replaced_count,
            'notes': notes,
        },
    }


def _hit_any(text: str, keywords: List[str]) -> bool:
    return any(k in text for k in keywords)


def _is_animal_food(name: str) -> bool:
    animal_kw = ['羊肉', '牛肉', '鸡肉', '鸭肉', '猪肉', '鱼', '虾', '蟹', '蛋', '奶']
    return any(k in name for k in animal_kw)
