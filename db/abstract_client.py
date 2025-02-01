from abc import ABC, abstractmethod


class AbstractClient(ABC):
    """Abstract class to define the interface of a database client"""
    @abstractmethod
    def connect(self):
        """Connects to the database"""
        pass

    def list_database_names(self):
        """Lists the names of available databases"""
        pass

    @abstractmethod
    def list_collection_names(self, database_name):
        """Lists the names of all collections (or tables) in a database"""
        pass

    @abstractmethod
    def fetch_documents(self, database_name, collection_name, order_by=None, sort_order=1, filter_query=None, limit=10, skip=0):
        """Fetches documents (or records) in a collection (or table)"""
        pass

    @abstractmethod
    def insert_document(self, database_name, collection_name, document):
        """Inserts a document (or record) into a collection (or table)"""
        pass

    @abstractmethod
    def delete_document(self, database_name, collection_name, document):
        """Deletes a document (or record) from a collection (or table)"""
        pass

    @abstractmethod
    def update_document(self, database_name, collection_name, filter_query, update_query):
        """Updates a document (or record) in a collection (or table)"""
        pass

    @abstractmethod
    def get_type_converters(self):
        """Returns a dictionary with data types and associated conversion functions"""
        pass

    @abstractmethod
    def get_collection_schema(self, database_name, collection_name, sample_size=10):
        """Returns the schema of a collection (or table)"""
        pass

    @abstractmethod
    def execute_raw_query(self, query):
        """Executes a raw query and returns the results"""
        pass

    @abstractmethod
    def get_syntax_highlighter(self):
        """Returns a syntax highlighter for the query editor"""
        pass
