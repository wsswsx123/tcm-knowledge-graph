from .. import neo4j_graph

class Neo4jNode:
    @staticmethod
    def get_all():
        query = "MATCH (n) RETURN n"
        return neo4j_graph.run(query).data()

    @staticmethod
    def get_by_id(node_id):
        query = "MATCH (n {id: $id}) RETURN n"
        return neo4j_graph.run(query, id=node_id).data()

    @staticmethod
    def delete(node_id):
        query = "MATCH (n {id: $id}) DETACH DELETE n"
        neo4j_graph.run(query, id=node_id)

class Neo4jEdge:
    @staticmethod
    def get_all():
        query = "MATCH ()-[r]->() RETURN r"
        return neo4j_graph.run(query).data()