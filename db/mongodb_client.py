import ast
import datetime
import bson
from pymongo import MongoClient
import pymongo
from db.abstract_client import AbstractClient


class MongoDBClient(AbstractClient):
    def __init__(self, uri: str = "mongodb://localhost:27017"):
        self.uri = uri
        self.client = None

    def connect(self):
        """Connects to MongoDB and returns the client"""
        try:
            self.client = MongoClient(self.uri)
            return self.client
        except Exception as e:
            raise Exception(f"Error connecting to MongoDB: {e}")

    def list_database_names(self):
        """Lists all available databases"""
        if not self.client:
            raise Exception("Client not connected to MongoDB.")
        return self.client.list_database_names()

    def list_collection_names(self, database_name: str):
        """Lists all collections in a database"""
        if not self.client:
            raise Exception("Client not connected to MongoDB.")
        db = self.client[database_name]
        return db.list_collection_names()

    def fetch_documents(self, database_name, collection_name, order_by=None, sort_order=1, filter_query=None, limit=10, skip=0):
        """Fetches documents from a collection"""
        if not self.client:
            raise Exception("Client not connected to MongoDB.")
        if filter_query is not None:
            try:
                filter_query = ast.literal_eval(filter_query)
            except Exception as e:
                raise ValueError(f"Error parsing filter query: {e}")

        db = self.client[database_name]

        if order_by:
            s_order = pymongo.ASCENDING if sort_order == 1 else pymongo.DESCENDING
            return list(db[collection_name]
                        .find(filter_query or {})
                        .sort(order_by, s_order)
                        .skip(skip)
                        .limit(limit))

        return list(db[collection_name].find(filter_query or {}).skip(skip).limit(limit))

    def insert_document(self, database_name, collection_name, document):
        """Inserts a document into a collection"""
        if not self.client:
            raise Exception("Client not connected to MongoDB.")
        db = self.client[database_name]

        return db[collection_name].insert_one(document).inserted_id

    def delete_document(self, database_name, collection_name, document):
        """Deletes a document from a collection"""
        if not self.client:
            raise Exception("Client not connected to MongoDB.")
        db = self.client[database_name]
        return db[collection_name].delete_one(document).deleted_count > 0

    def update_document(self, database_name, collection_name, filter_query, property):
        """Updates a document in a collection"""
        if not self.client:
            raise Exception("Client not connected to MongoDB.")
        db = self.client[database_name]
        new_values = {"$set": property}
        return db[collection_name].update_one(filter_query, new_values).modified_count > 0

    def get_type_converters(self):
        """Returns a dictionary with data types and associated conversion functions"""

        return {
            int: lambda value: int(value),
            float: lambda value: float(value),
            bool: lambda value: value.lower() in ["true", "1"],
            dict: lambda value: ast.literal_eval(value),
            bson.objectid.ObjectId: lambda value: bson.objectid.ObjectId(value),
            str: lambda value: value,
            datetime: lambda value: datetime.fromisoformat(value),
        }

    def get_collection_schema(self, database_name, collection_name, sample_size=10):
        """Returns the schema of a collection"""
        if not self.client:
            raise Exception("Client not connected to MongoDB.")
        db = self.client[database_name]
        collection = db[collection_name]
        documents = collection.find().limit(sample_size)
        schema = {}
        for doc in documents:
            for field, value in doc.items():
                # If the field is already in the schema, ensure consistency
                if field in schema:
                    if schema[field] != type(value):
                        schema[field] = object  # Fallback to generic type if inconsistent
                else:
                    # Add new field to schema
                    schema[field] = type(value)
        return schema

    def execute_raw_query(self, raw_command):
        """
        Executes a MongoDB operation in the format: database_name.collection_name.operation(params).
        Example input: nosql_manager_test.products.insert_one({"id": 104, "name": "Keyboard", "price": 75.0, "stock": 20})
        """
        if not self.client:
            raise Exception("Client not connected to MongoDB.")

        try:
            # Split the raw_command into parts: database, collection, and operation
            parts = raw_command.split(".", 2)
            if len(parts) < 3:
                raise ValueError("Query must be in the format: database_name.collection_name.operation(params)")

            database_name, collection_name, operation_call = parts

            # Extract the operation and parameters
            operation, params = operation_call.split("(", 1)
            params = params.rstrip(")")  # Remove the closing parenthesis

            # Parse the parameters into a Python dictionary or list
            if params.strip():
                params = ast.literal_eval(params)  # Safely convert string to dict or list
            else:
                params = {}

            # Access the database and collection
            db = self.client[database_name]
            collection = db[collection_name]

            # Dynamically call the MongoDB collection operation
            if hasattr(collection, operation):
                method = getattr(collection, operation)

                # Check if params is a dict (e.g., for find, insert, update, etc.)
                if isinstance(params, dict):
                    result = method(params)  # Pass as a positional argument
                elif isinstance(params, list):
                    result = method(*params)  # Unpack as multiple positional arguments
                elif isinstance(params, tuple):
                    # If params are tuple-based (e.g., `update_one`), unpack them
                    result = method(*params)
                else:
                    result = method()

                if isinstance(result, pymongo.cursor.Cursor):
                    return list(result)  # Convert cursor to list
                else:
                    # Dynamically collect attributes from the result object
                    attributes = [{
                        "acknowledged": getattr(result, "acknowledged", None),
                        "inserted_id": str(getattr(result, "inserted_id", None)),
                        "matched_count": getattr(result, "matched_count", None),
                        "modified_count": getattr(result, "modified_count", None),
                        "deleted_count": getattr(result, "deleted_count", None),
                    }]

                    # Filter out None values for cleaner results
                    return attributes
            else:
                raise ValueError(f"Unsupported operation: {operation}")

        except Exception as e:
            raise Exception(f"Error executing raw query: {e}")

    def get_syntax_highlighter(self):
        """Returns a syntax highlighter for the query editor"""
        return {
            "keywords": [
                "find", "insert_one", "insert_many", "update_one",
                "update_many", "delete_one", "delete_many", "aggregate",
                "count_documents", "distinct", "bulk_write", "create_index",
                "drop_index", "list_indexes", "watch"
            ],
            "operators": [
                "$eq", "$ne", "$gt", "$gte", "$lt", "$lte", "$in", "$nin",
                "$exists", "$type", "$regex", "$expr", "$mod", "$text", "$search",
                "$where", "$all", "$size", "$bitsAllSet", "$bitsAnySet",
                "$and", "$or", "$not",
                "$add", "$subtract", "$multiply", "$divide", "$mod"
            ],
            "comments": {
                "line": ["//"],
                "block": [{"/*": "*/"}]
            },
            "config": {
                "keyword": {"foreground": "orange", "font": ("Courier", 10, "bold")},
                "string": {"foreground": "green"},
                "number": {"foreground": "blue"},
                "comment": {"foreground": "gray", "font": ("Courier", 10, "italic")},
                "operator": {"foreground": "red"},
            }
        }
