# run_create_kg.py
from neo4j import GraphDatabase
import random
import os

# ========== 修改这里的密码（或通过环境变量 NEO4J_PASSWORD 传入） ==========
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = os.environ.get('NEO4J_PASSWORD', 'your_password')
# ==================================

# 体质数据
constitutions = [
    ('c_pinghe', '平和质', '阴阳气血调和，以体态适中、面色红润、精力充沛等为主要特征。'),
    ('c_qixu', '气虚质', '元气不足，以疲乏、气短、自汗等气虚表现为主要特征。'),
    ('c_yangxu', '阳虚质', '阳气不足，以畏寒怕冷、手足不温等虚寒表现为主要特征。'),
    ('c_yinxu', '阴虚质', '阴液亏少，以口燥咽干、手足心热等虚热表现为主要特征。'),
    ('c_tanshi', '痰湿质', '痰湿凝聚，以形体肥胖、腹部肥满、口黏苔腻等痰湿表现为主要特征。'),
    ('c_shire', '湿热质', '湿热内蕴，以面垢油光、口苦、苔黄腻等湿热表现为主要特征。'),
    ('c_xueyu', '血瘀质', '血行不畅，以肤色晦黯、舌质紫黯等血瘀表现为主要特征。'),
    ('c_qiyu', '气郁质', '气机郁滞，以神情抑郁、忧虑脆弱等气郁表现为主要特征。'),
    ('c_tebing', '特禀质', '先天失常，以生理缺陷、过敏反应等为主要特征。')
]

# 穴位名称池
acupoint_names = [
    '足三里', '关元', '气海', '中脘', '天枢', '大椎', '命门', '肾俞', '脾俞', '肺俞',
    '心俞', '肝俞', '胆俞', '大肠俞', '小肠俞', '三阴交', '阴陵泉', '阳陵泉', '太溪', '太冲',
    '涌泉', '行间', '内关', '外关', '合谷', '曲池', '肩井', '风池', '百会', '神阙'
]
locations = ['小腿外侧', '下腹部', '背部', '腰部', '胸部', '头部', '手部', '足部', '前臂', '上臂']
methods = ['按揉', '艾灸', '针刺', '拔罐', '刮痧', '指压', '热敷']

# 食材名称池
food_names = [
    '山药', '薏米', '红豆', '绿豆', '黑豆', '黄豆', '小米', '大米', '糯米', '小麦',
    '大麦', '燕麦', '荞麦', '玉米', '红薯', '土豆', '芋头', '莲藕', '百合', '银耳',
    '木耳', '香菇', '蘑菇', '金针菇', '猴头菇', '红枣', '枸杞', '桂圆', '莲子', '芡实'
]
natures = ['温', '热', '寒', '凉', '平', '微温', '微寒']
effects = ['补气', '补血', '滋阴', '壮阳', '健脾', '祛湿', '清热', '解毒', '活血', '化瘀']

# 运动名称池
exercise_names = ['八段锦', '太极拳', '五禽戏', '易筋经', '六字诀', '站桩', '散步', '慢跑', '快走', '游泳']
exercise_effects = ['调理脏腑', '疏通经络', '增强体质', '调和气血', '平衡阴阳']
exercise_methods = ['每日1次', '每周3-5次', '每次20分钟', '每次30分钟', '清晨练习']

NUM_ACUPOINTS = 500
NUM_FOODS = 500
NUM_EXERCISES = 500

def run_cypher(driver, statements):
    with driver.session() as session:
        for stmt in statements:
            if not stmt.strip():
                continue
            try:
                session.run(stmt)
                print(f"✓ {stmt[:60]}...")
            except Exception as e:
                print(f"✗ 失败: {stmt[:60]}... 错误: {e}")

def main():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    try:
        driver.verify_connectivity()
        print("连接成功")
    except Exception as e:
        print(f"连接失败: {e}")
        return

    statements = []

    # 1. 清空
    statements.append("MATCH (n) DETACH DELETE n")

    # 2. 体质节点
    for cid, name, desc in constitutions:
        statements.append(f"CREATE ({cid}:Constitution {{id:'{cid}', name:'{name}', description:'{desc}'}})")

    # 3. 穴位节点
    for i in range(NUM_ACUPOINTS):
        base = acupoint_names[i % len(acupoint_names)]
        suffix = i // len(acupoint_names)
        name = f"{base}{suffix+1}" if suffix > 0 else base
        loc = random.choice(locations) + f" {random.randint(1,5)}寸"
        method = random.choice(methods) + f"{random.randint(5,30)}分钟"
        statements.append(f"CREATE (a_{i}:Acupoint {{id:'acupoint_{i}', name:'{name}', location:'{loc}', method:'{method}'}})")

    # 4. 食材节点
    for i in range(NUM_FOODS):
        base = food_names[i % len(food_names)]
        suffix = i // len(food_names)
        name = f"{base}{suffix+1}" if suffix > 0 else base
        nature = random.choice(natures)
        effect = random.choice(effects) + "、" + random.choice(effects)
        statements.append(f"CREATE (f_{i}:Food {{id:'food_{i}', name:'{name}', nature:'{nature}', effect:'{effect}'}})")

    # 5. 运动节点
    for i in range(NUM_EXERCISES):
        base = exercise_names[i % len(exercise_names)]
        suffix = i // len(exercise_names)
        name = f"{base}{suffix+1}" if suffix > 0 else base
        effect = random.choice(exercise_effects)
        method = random.choice(exercise_methods)
        statements.append(f"CREATE (e_{i}:Exercise {{id:'exercise_{i}', name:'{name}', effect:'{effect}', method:'{method}'}})")

    # 6. 体质-穴位关系（每个体质随机分配约55个）
    for cid, _, _ in constitutions:
        indices = random.sample(range(NUM_ACUPOINTS), NUM_ACUPOINTS // 9 + 10)
        for idx in indices:
            statements.append(f"MATCH (c:Constitution {{id:'{cid}'}}), (a:Acupoint {{id:'acupoint_{idx}'}}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a)")

    # 7. 体质-食材关系
    for cid, _, _ in constitutions:
        indices = random.sample(range(NUM_FOODS), NUM_FOODS // 9 + 10)
        for idx in indices:
            statements.append(f"MATCH (c:Constitution {{id:'{cid}'}}), (f:Food {{id:'food_{idx}'}}) CREATE (c)-[:RECOMMEND_FOOD]->(f)")

    # 8. 体质-运动关系
    for cid, _, _ in constitutions:
        indices = random.sample(range(NUM_EXERCISES), NUM_EXERCISES // 9 + 10)
        for idx in indices:
            statements.append(f"MATCH (c:Constitution {{id:'{cid}'}}), (e:Exercise {{id:'exercise_{idx}'}}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e)")

    # 9. 疗法过程节点及关系
    for cid, name, _ in constitutions:
        tp_id = f"tp_{cid[2:]}"
        statements.append(f"CREATE ({tp_id}:TherapyProcess {{id:'{tp_id}', name:'{name}艾灸疗法', base:'清洁皮肤，取舒适体位', sequence:'大椎→足三里→关元', frequency:'每周3次，4周一疗程'}})")
        statements.append(f"MATCH (c:Constitution {{id:'{cid}'}}), (tp:TherapyProcess {{id:'{tp_id}'}}) CREATE (c)-[:HAS_THERAPY]->(tp)")

    # 10. 养生知识节点及关系
    for cid, name, _ in constitutions:
        for cat in ['饮食调养', '起居调摄', '运动保健', '药物调养']:
            hk_id = f"hk_{cid[2:]}_{cat}"
            content = f"{name}的{cat}建议：请根据个人情况选择适宜方法。"
            statements.append(f"CREATE ({hk_id}:HealthKnowledge {{id:'{hk_id}', type:'{name}', category:'{cat}', content:'{content}'}})")
            statements.append(f"MATCH (c:Constitution {{id:'{cid}'}}), (hk:HealthKnowledge {{id:'{hk_id}'}}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk)")

    # 可选：统计
    statements.append("MATCH (n) RETURN labels(n) AS 类型, count(n) AS 数量")

    # 执行
    print(f"共 {len(statements)} 条语句，开始执行...")
    run_cypher(driver, statements)
    print("完成！")

    driver.close()

if __name__ == "__main__":
    main()