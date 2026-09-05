from flask import Blueprint, jsonify, current_app
import json

bp = Blueprint('graph', __name__, url_prefix='/api/graph')

def process_graph_data(records):
    """
    将Neo4j查询结果转换为前端ECharts可用的节点和链接格式。
    使用node.items()安全提取属性，并添加category字段（节点标签）。
    """
    nodes = set()
    links = []
    for record in records:
        # 处理节点（可能是 'n' 或 'c'）
        for key in ('n', 'c'):
            if key in record and record[key] is not None:
                node = record[key]
                # 从node中提取属性，只保留JSON可序列化的基本类型
                props = {}
                for k, v in node.items():
                    if isinstance(v, (str, int, float, bool, type(None))):
                        props[k] = v
                    else:
                        try:
                            json.dumps(v)
                            props[k] = v
                        except TypeError:
                            props[k] = str(v)
                # 添加category字段，取节点第一个标签（如果有）
                if node.labels:
                    props['category'] = list(node.labels)[0]
                else:
                    props['category'] = 'Unknown'
                nodes.add(json.dumps(props, ensure_ascii=False))

        # 处理关系
        if 'r' in record and record['r'] is not None:
            rel = record['r']
            try:
                start_id = rel.start_node['id']
                end_id = rel.end_node['id']
                links.append({
                    'source': str(start_id),
                    'target': str(end_id),
                    'label': str(rel.type)
                })
            except (KeyError, AttributeError) as e:
                print(f"跳过关系（缺少ID）: {e}")
                continue

    # 将JSON字符串还原为字典列表
    node_list = []
    for node_str in nodes:
        try:
            node_list.append(json.loads(node_str))
        except json.JSONDecodeError:
            print(f"节点JSON解析失败: {node_str}")
            continue

    return node_list, links

@bp.route('', methods=['GET'])
def get_full_graph():
    """
    获取完整知识图谱：所有节点及其关系。
    """
    try:
        graph = current_app.neo4j_graph
        query = "MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN n, r, m"
        data = graph.run(query).data()
        nodes, links = process_graph_data(data)
        return jsonify({'nodes': nodes, 'links': links})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@bp.route('/<constitution>', methods=['GET'])
def get_constitution_graph(constitution):
    """
    获取特定体质的关联图谱（体质节点及其一度关联的节点和关系）。
    """
    try:
        graph = current_app.neo4j_graph
        node_id = f"c_{constitution}"
        query = "MATCH (c:Constitution {id: $node_id})-[r]-(n) RETURN c, r, n"
        data = graph.run(query, node_id=node_id).data()
        nodes, links = process_graph_data(data)
        return jsonify({'nodes': nodes, 'links': links})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500