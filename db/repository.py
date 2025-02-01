from business.config import Config

class Repository:
    def __init__(self, client, database_name):
        """
        Initializes the repository with a client (MongoDBClient, MockClient, etc.)
        and the selected database name.
        """
        self.client = client
        self.database_name = database_name
        
    def connect(self):
        """Connects to the client"""
        self.client.connect()
        if getattr(self.client, "uri", None) is not None:
            Config.get_instance().add_connection(self.client.uri)
            Config.get_instance().set_last_connection(self.client.uri)
        return True

    def set_database_name(self, database_name):
        """Sets the database name"""
        self.database_name = database_name

    def list_database_names(self):
        """Lists the names of the databases through the client"""
        return self.client.list_database_names()

    def fetch_documents(self, collection_name, order_by=None, sort_order=1, filter_query=None, limit=10, skip=0):
        """Fetches documents in a collection through the client"""
        return self.client.fetch_documents(self.database_name, collection_name, order_by, sort_order, filter_query, limit, skip)

    def insert_document(self, collection_name, document):
        """Inserts a document into a collection through the client"""
        return self.client.insert_document(self.database_name, collection_name, document)

    def list_collections(self):
        """Lists the collections of the database"""
        return self.client.list_collection_names(self.database_name)
    
    def delete_document(self, collection_name, document):
        """Deletes a document from a collection through the client"""
        return self.client.delete_document(self.database_name, collection_name, document)
    
    def update_document(self, collection_name, filter_query, update_query):
        """Updates a document in a collection through the client"""
        return self.client.update_document(self.database_name, collection_name, filter_query, update_query)
    
    def get_type_converters(self):
        """Returns the client's type converters"""
        return self.client.get_type_converters()
    
    def get_collection_schema(self, collection_name, sample_size=10):
        """Returns the schema of a collection"""
        return self.client.get_collection_schema(self.database_name, collection_name, sample_size)
    
    def execute_raw_query(self, query):
        """Executes a raw query through the client"""
        return self.client.execute_raw_query(query)
    
    def get_syntax_highlighter(self):
        """Returns the syntax highlighter for the client"""
        return self.client.get_syntax_highlighter()