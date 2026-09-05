from flask import Blueprint, jsonify, request, current_app
import json

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 获取所有节点和关系
@bp.route('/graph', methods=['GET'])
def get_graph():
    graph = current_app.neo4j_graph

    # 查询所有节点
    nodes_data = graph.run("MATCH (n) RETURN n").data()
    nodes = []
    for record in nodes_data:
        node = dict(record['n'])
        # 确保节点包含 name 字段，若缺失则设为默认值
        if 'name' not in node or not node['name']:
            node['name'] = '未命名'
        # 提取节点标签（取第一个标签作为类别）
        labels = list(record['n'].labels)
        node['label'] = labels[0] if labels else 'Unknown'
        nodes.append(node)

    # 查询所有关系，同时返回源和目标节点的 ID 以及关系类型
    edges_data = graph.run("""
        MATCH (a)-[r]->(b)
        RETURN a.id AS source, b.id AS target, type(r) AS type, r
    """).data()

    edges = []
    for idx, record in enumerate(edges_data):
        # 如果关系本身有 id 属性则使用，否则生成临时 ID
        rel_id = record.get('r', {}).get('id', f'temp_{idx}')
        edges.append({
            'id': rel_id,
            'source': record['source'],
            'target': record['target'],
            'type': record['type']
        })

    return jsonify({
        'nodes': nodes,
        'edges': edges
    })

# 删除节点（同时删除关联关系）
@bp.route('/node/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    graph = current_app.neo4j_graph
    graph.run("MATCH (n {id: $id}) DETACH DELETE n", id=node_id)
    return jsonify({'success': True})

# 添加节点
@bp.route('/node', methods=['POST'])
def add_node():
    data = request.json
    node_id = data.get('id')
    label = data.get('label')
    name = data.get('name')
    properties = data.get('properties', {})

    if not all([node_id, label, name]):
        return jsonify({'error': '缺少必要字段'}), 400

    allowed_labels = ['Constitution', 'Acupoint', 'Food', 'Exercise']
    if label not in allowed_labels:
        return jsonify({'error': '标签类型不允许'}), 400

    graph = current_app.neo4j_graph
    query = f"""
    CREATE (n:`{label}` {{id: $id, name: $name, properties: $properties}})
    RETURN n
    """
    try:
        graph.run(query, id=node_id, name=name, properties=json.dumps(properties, ensure_ascii=False)).data()
        return jsonify({'success': True, 'id': node_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新节点（只更新名称和属性，ID和标签不可变）
@bp.route('/node/<node_id>', methods=['PUT'])
def update_node(node_id):
    data = request.json
    name = data.get('name')
    properties = data.get('properties', {})

    if not name:
        return jsonify({'error': '名称不能为空'}), 400

    graph = current_app.neo4j_graph
    # 先检查节点是否存在
    check = graph.run("MATCH (n {id: $id}) RETURN n", id=node_id).data()
    if not check:
        return jsonify({'error': '节点不存在'}), 404

    # 更新节点的 name 和 properties
    query = """
    MATCH (n {id: $id})
    SET n.name = $name, n.properties = $properties
    RETURN n
    """
    try:
        graph.run(query, id=node_id, name=name, properties=json.dumps(properties, ensure_ascii=False)).data()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 添加关系
@bp.route('/edge', methods=['POST'])
def add_edge():
    data = request.json
    source = data.get('source')
    target = data.get('target')
    rel_type = data.get('type')

    if not all([source, target, rel_type]):
        return jsonify({'error': '缺少必要字段'}), 400

    allowed_rels = ['RECOMMEND_ACUPOINT', 'RECOMMEND_FOOD', 'RECOMMEND_EXERCISE']
    if rel_type not in allowed_rels:
        return jsonify({'error': '关系类型不允许'}), 400

    graph = current_app.neo4j_graph
    query = f"""
    MATCH (a {{id: $source}}), (b {{id: $target}})
    CREATE (a)-[r:`{rel_type}`]->(b)
    RETURN r
    """
    try:
        graph.run(query, source=source, target=target).data()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500