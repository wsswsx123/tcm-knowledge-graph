# backend/app/services/kg_fallback.py
"""Neo4j 不可用时的静态知识底库（五级容错第 5 级）。"""

STATIC_RECS = {
    'qixu': {
        'acupoints': [
            {'name': '足三里', 'location': '犊鼻下 3 寸', 'method': '按揉 5 分钟'},
            {'name': '气海', 'location': '脐下 1.5 寸', 'method': '艾灸或按揉'},
            {'name': '关元', 'location': '脐下 3 寸', 'method': '温和灸'},
        ],
        'foods': [
            {'name': '山药', 'nature': '平', 'effect': '补脾益气'},
            {'name': '红枣', 'nature': '温', 'effect': '补中益气'},
            {'name': '小米', 'nature': '平', 'effect': '健脾和胃'},
        ],
        'exercises': [
            {'name': '八段锦', 'effect': '调和气血', 'method': '每日 1 次'},
            {'name': '散步', 'effect': '畅通气机', 'method': '每次 20-30 分钟'},
        ],
        'precautions': ['避免过度劳累', '饮食宜温软'],
    },
    'yangxu': {
        'acupoints': [
            {'name': '命门', 'location': '第二腰椎棘突下', 'method': '温和灸'},
            {'name': '关元', 'location': '脐下 3 寸', 'method': '艾灸'},
            {'name': '肾俞', 'location': '第二腰椎旁开 1.5 寸', 'method': '按揉或灸'},
        ],
        'foods': [
            {'name': '羊肉', 'nature': '温', 'effect': '温补肾阳'},
            {'name': '桂圆', 'nature': '温', 'effect': '补益心脾'},
            {'name': '生姜', 'nature': '温', 'effect': '温中散寒'},
        ],
        'exercises': [
            {'name': '太极拳', 'effect': '温通经脉', 'method': '每日练习'},
        ],
        'precautions': ['避风寒', '少食生冷'],
    },
    'yinxu': {
        'acupoints': [
            {'name': '太溪', 'location': '内踝与跟腱之间', 'method': '按揉'},
            {'name': '三阴交', 'location': '内踝上 3 寸', 'method': '按揉'},
            {'name': '涌泉', 'location': '足底前 1/3 凹陷', 'method': '搓揉至发热'},
        ],
        'foods': [
            {'name': '百合', 'nature': '微寒', 'effect': '养阴润肺'},
            {'name': '银耳', 'nature': '平', 'effect': '滋阴润燥'},
            {'name': '枸杞', 'nature': '平', 'effect': '滋补肝肾'},
        ],
        'exercises': [
            {'name': '六字诀', 'effect': '调息养阴', 'method': '动作宜缓'},
        ],
        'precautions': ['少熬夜', '忌辛辣燥热'],
    },
    'tanshi': {
        'acupoints': [
            {'name': '丰隆', 'location': '外踝上 8 寸', 'method': '按揉'},
            {'name': '阴陵泉', 'location': '胫骨内侧髁下缘', 'method': '按揉'},
            {'name': '中脘', 'location': '脐上 4 寸', 'method': '按揉'},
        ],
        'foods': [
            {'name': '薏米', 'nature': '凉', 'effect': '健脾祛湿'},
            {'name': '冬瓜', 'nature': '凉', 'effect': '利水渗湿'},
            {'name': '陈皮', 'nature': '温', 'effect': '理气化痰'},
        ],
        'exercises': [
            {'name': '快走', 'effect': '运化痰湿', 'method': '每周 5 次'},
        ],
        'precautions': ['少油腻甜食', '控制体重'],
    },
    'shire': {
        'acupoints': [
            {'name': '曲池', 'location': '肘横纹外侧', 'method': '按揉'},
            {'name': '阴陵泉', 'location': '胫骨内侧髁下缘', 'method': '按揉'},
            {'name': '合谷', 'location': '手背第 1、2 掌骨间', 'method': '按揉'},
        ],
        'foods': [
            {'name': '绿豆', 'nature': '寒', 'effect': '清热解毒'},
            {'name': '苦瓜', 'nature': '寒', 'effect': '清热泻火'},
            {'name': '薏米', 'nature': '凉', 'effect': '清热利湿'},
        ],
        'exercises': [
            {'name': '游泳', 'effect': '清热疏利', 'method': '适度即可'},
        ],
        'precautions': ['忌辛辣油炸', '保持二便通畅'],
    },
    'xueyu': {
        'acupoints': [
            {'name': '血海', 'location': '髌骨内上缘上 2 寸', 'method': '按揉'},
            {'name': '膈俞', 'location': '第七胸椎旁开 1.5 寸', 'method': '按揉'},
            {'name': '太冲', 'location': '足背第 1、2 跖骨间', 'method': '按揉'},
        ],
        'foods': [
            {'name': '山楂', 'nature': '微温', 'effect': '活血化瘀'},
            {'name': '黑木耳', 'nature': '平', 'effect': '活血通络'},
            {'name': '玫瑰花', 'nature': '温', 'effect': '行气活血'},
        ],
        'exercises': [
            {'name': '易筋经', 'effect': '疏通经络', 'method': '动作舒展'},
        ],
        'precautions': ['避免久坐', '注意保暖'],
    },
    'qiyu': {
        'acupoints': [
            {'name': '太冲', 'location': '足背第 1、2 跖骨间', 'method': '按揉'},
            {'name': '内关', 'location': '腕横纹上 2 寸', 'method': '按揉'},
            {'name': '期门', 'location': '乳头直下第 6 肋间', 'method': '轻揉'},
        ],
        'foods': [
            {'name': '玫瑰花', 'nature': '温', 'effect': '疏肝解郁'},
            {'name': '佛手', 'nature': '温', 'effect': '理气和中'},
            {'name': '陈皮', 'nature': '温', 'effect': '理气健脾'},
        ],
        'exercises': [
            {'name': '五禽戏', 'effect': '调畅情志', 'method': '配合深呼吸'},
        ],
        'precautions': ['避免长期压抑情绪', '作息规律'],
    },
    'tebing': {
        'acupoints': [
            {'name': '足三里', 'location': '犊鼻下 3 寸', 'method': '按揉'},
            {'name': '肺俞', 'location': '第三胸椎旁开 1.5 寸', 'method': '轻揉'},
            {'name': '迎香', 'location': '鼻翼外缘中点旁', 'method': '按揉'},
        ],
        'foods': [
            {'name': '山药', 'nature': '平', 'effect': '益气固表'},
            {'name': '红枣', 'nature': '温', 'effect': '调和营卫'},
            {'name': '薏米', 'nature': '凉', 'effect': '健脾渗湿'},
        ],
        'exercises': [
            {'name': '八段锦', 'effect': '调和营卫', 'method': '动作轻柔'},
        ],
        'precautions': ['避开已知过敏原', '起居避风寒'],
    },
    'pinghe': {
        'acupoints': [
            {'name': '足三里', 'location': '犊鼻下 3 寸', 'method': '保健按揉'},
            {'name': '气海', 'location': '脐下 1.5 寸', 'method': '轻揉'},
        ],
        'foods': [
            {'name': '小米', 'nature': '平', 'effect': '健脾和胃'},
            {'name': '山药', 'nature': '平', 'effect': '平补脾胃'},
        ],
        'exercises': [
            {'name': '太极拳', 'effect': '调和阴阳', 'method': '长期坚持'},
        ],
        'precautions': ['饮食有节', '起居有常'],
    },
}


def get_static_recommendations(constitution: str) -> dict:
    recs = STATIC_RECS.get(constitution) or STATIC_RECS['pinghe']
    return {
        'acupoints': list(recs.get('acupoints', [])),
        'foods': list(recs.get('foods', [])),
        'exercises': list(recs.get('exercises', [])),
        'therapy_process': [],
        'health_knowledge': [],
        'precautions': list(recs.get('precautions', [])),
        'source': 'static_fallback',
    }
