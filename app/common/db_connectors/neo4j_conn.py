from neo4j import GraphDatabase
from decouple import config

NEO4J_URI = config("NEO4J_URI")
NEO4J_USERNAME = config("NEO4J_USERNAME")
NEO4J_PASSWORD = config("NEO4J_PASSWORD")
AURA_INSTANCEID = config("AURA_INSTANCEID")
AURA_INSTANCENAME = config("AURA_INSTANCENAME")

class Neo4jConnector:
    def __init__(self):
        uri = "bolt://localhost:7687" 
        user="neo4j"
        password="uademerypoc"
        # uri = NEO4J_URI
        # user=NEO4J_USERNAME
        # password=NEO4J_PASSWORD
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def try_connection(self):
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                for record in result:
                    print(record)
            print("Connection successful!")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        with self.driver.session() as session:
            session.write_transaction(self._create_node, label, properties)

    def get_node(self, label, key, value):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_node, label, key, value)
            return result
    
    def get_all_nodes(self, label):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_all_node, label)
            return result

    def update_node(self, label, key, value, properties):
        with self.driver.session() as session:
            session.write_transaction(self._update_node, label, key, value, properties)

    def delete_node(self, label, key, value):
        with self.driver.session() as session:
            session.write_transaction(self._delete_node, label, key, value)
    def create_relationship(self, start_node_label, start_node_key, start_node_value, 
                            relationship_type, end_node_label, end_node_key, end_node_value, 
                            properties=None):
        with self.driver.session() as session:
            session.write_transaction(self._create_relationship, start_node_label, start_node_key, start_node_value, 
                                      relationship_type, end_node_label, end_node_key, end_node_value, properties)
    def delete_relationship(self, start_node_label, start_node_key, start_node_value, 
                            relationship_type, end_node_label, end_node_key, end_node_value):
        with self.driver.session() as session:
            session.write_transaction(self._delete_relationship, start_node_label, start_node_key, start_node_value, 
                                      relationship_type, end_node_label, end_node_key, end_node_value)

    def get_nodes_with_property_greater_than_and_relationship(self, node_label, property_key, property_value, relationship_type, related_node_label, related_node_property_key, related_node_property_value):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_nodes_with_property_greater_than_and_relationship,
                                              node_label, property_key, property_value,
                                              relationship_type, related_node_label,
                                              related_node_property_key, related_node_property_value)
            return result
    
    def get_nodes_without_relationship(self, label, relationship_type):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_nodes_without_relationship, label, relationship_type)
            return result
    
    def get_nodes_with_relationship(self, node_label, relationship_type, related_node_label):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_nodes_with_relationship,
                                              node_label,
                                              relationship_type, related_node_label)
            return result
    
    def get_nodes_with_indirect_relationship(self, node_label, intermediate_relationship_type, intermediate_node_label, relationship_type, related_node_label, related_node_property_key, related_node_property_value):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_nodes_with_indirect_relationship,
                                              node_label, intermediate_relationship_type, intermediate_node_label, relationship_type, related_node_label, related_node_property_key, related_node_property_value)
            return result
    
    def get_nodes_with_direct_relationship(self, node_label, relationship_type, related_node_label, related_node_property_key, related_node_property_value):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_nodes_with_direct_relationship,
                                              node_label, relationship_type, related_node_label, related_node_property_key, related_node_property_value)
            return result


    @staticmethod
    def _create_node(tx, label, properties):
        query = f"CREATE (n:{label} {{"
        query += ", ".join([f"{key}: ${key}" for key in properties.keys()])
        query += "})"
        tx.run(query, **properties)

    @staticmethod
    def _get_node(tx, label, key, value):
        query = f"MATCH (n:{label} {{{key}: ${key}}}) RETURN n"
        result = tx.run(query, {key: value})
        return result.single()
    
    @staticmethod
    def _get_all_node(tx, label):
        query = f"MATCH (n:{label}) RETURN n"
        result = tx.run(query)
        return [record["n"] for record in result]


    @staticmethod
    def _update_node(tx, label, key, value, properties):
        query = f"MATCH (n:{label} {{{key}: ${key}}}) SET "
        query += ", ".join([f"n.{prop_key} = ${prop_key}" for prop_key in properties.keys()])
        tx.run(query, {key: value, **properties})

    @staticmethod
    def _delete_node(tx, label, key, value):
        query = f"MATCH (n:{label} {{{key}: ${key}}}) DETACH DELETE n"
        tx.run(query, {key: value})

    @staticmethod
    def _create_relationship(tx, start_node_label, start_node_key, start_node_value, 
                             relationship_type, end_node_label, end_node_key, end_node_value, 
                             properties=None):
        query = (f"MATCH (a:{start_node_label} {{{start_node_key}: $start_value}}), "
                 f"(b:{end_node_label} {{{end_node_key}: $end_value}}) "
                 f"CREATE (a)-[r:{relationship_type} {{")
        if properties:
            query += ", ".join([f"{key}: ${key}" for key in properties.keys()])
        query += "}]->(b)"
        params = { "start_value": start_node_value, "end_value": end_node_value }
        if properties:
            params.update(properties)
        tx.run(query, params)
    
    @staticmethod
    def _delete_relationship(tx, start_node_label, start_node_key, start_node_value, 
                             relationship_type, end_node_label, end_node_key, end_node_value):
        query = (f"MATCH (a:{start_node_label} {{{start_node_key}: $start_value}})-[r:{relationship_type}]-(b:{end_node_label} {{{end_node_key}: $end_value}}) "
                 f"DELETE r")
        tx.run(query, {"start_value": start_node_value, "end_value": end_node_value})

    @staticmethod
    def _get_nodes_with_property_greater_than_and_relationship(tx, node_label, property_key, property_value, relationship_type, related_node_label, related_node_property_key, related_node_property_value):
        query = (f"MATCH (n:{node_label})-[r:{relationship_type}]-(m:{related_node_label} {{{related_node_property_key}: $related_node_property_value}}) "                 
                 f"WHERE n.{property_key} >= $property_value "                 
                 f"RETURN n")
        result = tx.run(query, {"property_value": property_value, "related_node_property_value": related_node_property_value})
        return [record["n"] for record in result]
    
    @staticmethod
    def _get_nodes_without_relationship(tx, label, relationship_type):
        query = f"MATCH (n:{label}) WHERE NOT (n)-[:{relationship_type}]-() RETURN n"
        result = tx.run(query)
        return [record["n"] for record in result]
    
    @staticmethod
    def _get_nodes_with_relationship(tx, node_label, relationship_type, related_node_label):
        query = (f"MATCH (n:{node_label})-[r:{relationship_type}]-(m:{related_node_label}) "                 
                 f"RETURN n")
        result = tx.run(query)
        return [record["n"] for record in result]
    
    @staticmethod
    def _get_nodes_with_indirect_relationship(tx, node_label, intermediate_relationship_type, intermediate_node_label, relationship_type, related_node_label,related_node_property_key, related_node_property_value):
        query = (f"MATCH (n:{node_label})-[ri:{intermediate_relationship_type}]-(i:{intermediate_node_label}) "
                 f"-[r:{relationship_type}]-(m:{related_node_label} {{{related_node_property_key}: $related_node_property_value}}) "                 
                 f"RETURN n")
        result = tx.run(query, { "related_node_property_value": related_node_property_value})
        return [record["n"] for record in result]
    @staticmethod
    def _get_nodes_with_direct_relationship(tx, node_label, relationship_type, related_node_label,related_node_property_key, related_node_property_value):
        query = (f"MATCH (n:{node_label})"
                 f"-[r:{relationship_type}]-(m:{related_node_label} {{{related_node_property_key}: $related_node_property_value}}) "                 
                 f"RETURN n")
        result = tx.run(query, { "related_node_property_value": related_node_property_value})
        return [record["n"] for record in result] 