from flask import Blueprint, jsonify

from ..services.neo4j_client import get_graph, degraded_response

bp = Blueprint('recommend', __name__, url_prefix='/api/recommend')

@bp.route('/<constitution>', methods=['GET'])
def get_recommendations(constitution):
    graph = get_graph()
    if graph is None:
        return degraded_response()
    node_id = f"c_{constitution}"
    query = """
    MATCH (c:Constitution {id: $node_id})-[r]->(n)
    RETURN n, type(r) as rel_type
    """
    data = graph.run(query, node_id=node_id).data()
    result = {'acupoints': [], 'foods': [], 'exercises': []}
    for record in data:
        node = dict(record['n'])
        rel = record['rel_type']
        if 'ACUPOINT' in rel:
            result['acupoints'].append(node)
        elif 'FOOD' in rel:
            result['foods'].append(node)
        elif 'EXERCISE' in rel:
            result['exercises'].append(node)
    return jsonify(result)