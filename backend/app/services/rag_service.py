# backend/app/services/rag_service.py
from py2neo import Graph
import logging

logger = logging.getLogger(__name__)


class KGRetriever:
    """知识图谱检索服务"""

    def __init__(self, graph):
        self.graph = graph

    def get_recommendations(self, constitution: str) -> dict:
        """获取体质的基础推荐（扩展版，支持疗法过程和养生知识）"""
        node_id = f"c_{constitution}"

        query = """
        MATCH (c:Constitution {id: $node_id})-[r]->(n)
        RETURN n, type(r) as rel_type, labels(n) as labels
        """

        try:
            data = self.graph.run(query, node_id=node_id).data()

            result = {
                'acupoints': [],
                'foods': [],
                'exercises': [],
                'therapy_process': [],
                'health_knowledge': [],
                'precautions': []
            }
            for record in data:
                node = dict(record['n'])
                labels = record.get('labels', [])
                label = labels[0] if labels else ''

                if label == 'Acupoint':
                    result['acupoints'].append({
                        'name': node.get('name', ''),
                        'location': node.get('location', ''),
                        'method': node.get('method', '')
                    })
                elif label == 'Food':
                    result['foods'].append({
                        'name': node.get('name', ''),
                        'nature': node.get('nature', ''),
                        'effect': node.get('effect', '')
                    })
                elif label == 'Exercise':
                    result['exercises'].append({
                        'name': node.get('name', ''),
                        'effect': node.get('effect', ''),
                        'method': node.get('method', '')
                    })
                elif label == 'TherapyProcess':
                    result['therapy_process'].append({
                        'name': node.get('name', ''),
                        'base': node.get('base', ''),
                        'sequence': node.get('sequence', ''),
                        'frequency': node.get('frequency', '')
                    })
                elif label == 'HealthKnowledge':
                    result['health_knowledge'].append({
                        'category': node.get('category', ''),
                        'content': node.get('content', '')
                    })
                elif label == 'Precaution':
                    # 如果有单独的注意事项节点
                    result['precautions'].append(node.get('content', ''))
            return result
        except Exception as e:
            logger.error(f"图谱查询失败: {e}")
            return {'acupoints': [], 'foods': [], 'exercises': [], 'therapy_process': [], 'health_knowledge': [], 'precautions': []}

    def search_symptoms(self, query_text: str, limit: int = 5):
        """搜索相关症状（全文检索）"""
        try:
            cypher = """
            CALL db.index.fulltext.queryNodes('symptom_index', $query)
            YIELD node, score
            RETURN node, score
            ORDER BY score DESC
            LIMIT $limit
            """
            results = self.graph.run(cypher, query=query_text, limit=limit).data()
            return [dict(r['node']) for r in results]
        except Exception as e:
            logger.error(f"全文检索失败: {e}")
            return []