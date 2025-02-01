import ast
from db.abstract_client import AbstractClient

class MockClient(AbstractClient):
    def __init__(self, uri: str = ""):
        self.databases = {
            "mock_db": {
                "products": [
                    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 50},
                    {"id": 2, "name": "Phone", "price": 599.99, "stock": 100},
                ],
                "orders": [
                    {"id": 1, "product_id": 1, "quantity": 2},
                    {"id": 2, "product_id": 2, "quantity": 1},
                ]
            },
            "mock_db_2": {
                "users": [
                    {"id": 1, "name": "Alice", "email": "email1@teste.com"},
                    {"id": 2, "name": "Bob", "email": "email2@teste.com"},
                    {"id": 3, "name": "Charlie", "email": "email3@teste.com"},
                ]
            }
        }

    def connect(self):
        """Simulates database connection"""
        return self

    def list_database_names(self):
        """Lists simulated databases"""
        return list(self.databases.keys())

    def list_collection_names(self, database_name):
        """Lists simulated collections"""
        if database_name in self.databases:
            return list(self.databases[database_name].keys())
        return []

    def fetch_documents(self, database_name, collection_name, order_by=None, sort_order=1, filter_query=None, limit=10, skip=0):
        """Fetches simulated documents"""
        if database_name in self.databases:
            collection = self.databases[database_name].get(collection_name, [])
            if filter_query:
                query = ast.literal_eval(filter_query)
                collection = [doc for doc in collection if all(doc.get(key) == value for key, value in query.items())]
            if skip:
                collection = collection[skip:]

            if order_by:
                collection.sort(key=lambda doc: doc.get(order_by), reverse=sort_order < 0)

            return collection[:limit]  # Limits the number of results
        return []

    def insert_document(self, database_name, collection_name, document):
        """Inserts simulated documents"""
        if database_name in self.databases:
            self.databases[database_name].setdefault(collection_name, []).append(document)
            return len(self.databases[database_name][collection_name]) - 1
        return None
    
    def delete_document(self, database_name, collection_name, document):
        """Deletes simulated documents"""
        if database_name in self.databases:
            collection = self.databases[database_name].get(collection_name, [])
            for i, doc in enumerate(collection):
                if doc == document:
                    del collection[i]
                    return True
        return False
    
    def update_document(self, database_name, collection_name, filter_query, update_query):
        """Updates simulated documents"""
        if database_name in self.databases:
            collection = self.databases[database_name].get(collection_name, [])
            for doc in collection:
                if all(doc.get(key) == value for key, value in filter_query.items()):
                    doc.update(update_query)
                    return True
        return False
    
    def get_type_converters(self):
        """Returns a dictionary with data types and associated conversion functions"""
        return {
            int: lambda value: int(value),
            float: lambda value: float(value),
            bool: lambda value: value.lower() in ["true", "1"],
            str: lambda value: str(value),
        }
    
    def get_collection_schema(self, database_name, collection_name, sample_size=10):
        """Returns the schema of a simulated collection"""
        if database_name in self.databases:
            collection = self.databases[database_name].get(collection_name, [])
            schema = {}
            for doc in collection[:sample_size]:
                for field, value in doc.items():
                    schema[field] = type(value)
            return schema
        return {}
    
    def execute_raw_query(self, query):
        """Executes a raw query and returns the results"""
        raise NotImplementedError("Method not implemented for MockClient")
    
    get_syntax_highlighter = lambda self: None  # No syntax highlighter for mock client