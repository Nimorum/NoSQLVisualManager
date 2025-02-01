
class BusinessManager:
    def __init__(self, repository):
        self.repository = repository

    def connect(self):
        """Connects to MongoDB using the provided URI"""
        self.repository.connect()
        return self.repository

    def get_databases(self):
        """Returns the list of databases"""
        db_list = self.repository.list_database_names()
        return db_list

    def get_collections(self, database_name):
        """Returns the list of collections in a database"""
        self.repository.set_database_name(database_name)
        return self.repository.list_collections()

    def fetch_documents(self, database_name, collection_name, order_by=None, sort_order=1, query=None, limit=10, skip=0):
        """Fetches documents from a collection"""
        self.repository.set_database_name(database_name)
        return self.repository.fetch_documents(collection_name, order_by, sort_order, query, limit, skip)

    def insert_document(self, database_name, collection_name, document):
        """Inserts a document into a collection"""
        self.repository.set_database_name(database_name)
        schema = self.repository.get_collection_schema(collection_name)
        converters = self.repository.get_type_converters()
        converted_document = {}
        for field, value in document.items():
            # Get the expected type from the schema
            expected_type = schema.get(field, str)  # Default to str if the field type is unknown

            # Get the converter for the expected type
            converter = converters.get(expected_type)

            if converter:
                # Convert the value using the type converter
                try:
                    converted_document[field] = converter(value)
                except Exception as e:
                    raise ValueError(f"Error converting field '{field}' with value '{value}': {e}")
            else:
                # Fallback to the raw value if no converter is defined
                converted_document[field] = value

        return self.repository.insert_document(collection_name, converted_document)

    def delete_document(self, database_name, collection_name, document):
        """Deletes a document from a collection"""
        self.repository.set_database_name(database_name)
        return self.repository.delete_document(collection_name, document)

    def update_document(self, database_name, collection_name, document, updated_property):
        """Updates a document in a collection"""
        self.repository.set_database_name(database_name)
        schema = self.repository.get_collection_schema(collection_name)
        converters = self.repository.get_type_converters()

        value = document[updated_property]
        expected_type = schema.get(updated_property, str)  # Default to str if type is unknown
        converter = converters.get(expected_type)

        if converter:
            try:
                value = converter(value)
            except Exception as e:
                raise ValueError(f"Error converting value for field '{updated_property}': {e}")

        filter_query = {key: value for key, value in document.items() if key != updated_property}
        update_property = {updated_property: value}
        return self.repository.update_document(collection_name, filter_query, update_property)

    def execute_raw_query(self, query):
        """Executes a raw query"""
        return self.repository.execute_raw_query(query)

    def get_syntax_highlighter(self):
        """Returns the syntax highlighter for the query editor"""
        return self.repository.get_syntax_highlighter()
