import mysql.connector
from mysql.connector import Error
from db.abstract_client import AbstractClient
from db.syntax_highlight import syntax_highlight


class MySQLClient(AbstractClient):
    def __init__(self, uri: str = "mysql://root@localhost:3306"):
        self.uri = uri
        self.connection = None

    def connect(self):
        """Parses the URI and connects to the MySQL database"""
        try:
            # Parse URI for connection details
            from urllib.parse import urlparse
            parsed = urlparse(self.uri)

            self.connection = mysql.connector.connect(
                host=parsed.hostname,
                port=parsed.port or 3306,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path.lstrip("/") or None
            )
            if self.connection.is_connected():
                print("Connected to MySQL")
                return self.connection
        except Error as e:
            raise Exception(f"Error connecting to MySQL: {e}")

    def list_database_names(self):
        """Lists all available databases"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("Client not connected to MySQL.")
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        return [db[0] for db in cursor.fetchall()]

    def list_collection_names(self, database_name: str):
        """Lists all tables in a database"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("Client not connected to MySQL.")
        cursor = self.connection.cursor()
        cursor.execute(f"USE {database_name}")
        cursor.execute("SHOW TABLES")
        return [table[0] for table in cursor.fetchall()]

    def fetch_documents(self, database_name, table_name, order_by=None, sort_order="ASC", filter_query=None, limit=10, skip=0):
        """Fetches records from a table"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("Client not connected to MySQL.")
        query = f"SELECT * FROM {database_name}.{table_name}"
        if filter_query:
            query += f" WHERE {filter_query}"
        if order_by:
            query += f" ORDER BY {order_by} {sort_order}"
        query += f" LIMIT {limit} OFFSET {skip}"
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()

    def insert_document(self, database_name, table_name, document):
        """Inserts a record into a table"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("Client not connected to MySQL.")
        keys = ", ".join(document.keys())
        values = ", ".join(["%s"] * len(document))
        query = f"INSERT INTO {database_name}.{table_name} ({keys}) VALUES ({values})"
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(document.values()))
        self.connection.commit()
        return cursor.lastrowid

    def delete_document(self, database_name, table_name, document):
        """Deletes a record from a table"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("Client not connected to MySQL.")
        where_clause = " AND ".join([f"{key} = %s" for key in document.keys()])
        query = f"DELETE FROM {database_name}.{table_name} WHERE {where_clause}"
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(document.values()))
        self.connection.commit()
        return cursor.rowcount > 0

    def update_document(self, database_name, table_name, filter_query, property):
        """Updates records in a table"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("Client not connected to MySQL.")
        set_clause = ", ".join([f"{key} = %s" for key in property.keys()])
        str_filter_query = " AND ".join([f"{key} = %s" for key in filter_query.keys()])
        query = f"UPDATE {database_name}.{table_name} SET {set_clause} WHERE {str_filter_query}"
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(property.values()) + tuple(filter_query.values()))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_type_converters(self):
        """Returns a dictionary with data types and associated conversion functions"""
        return {
            int: lambda value: int(value),
            float: lambda value: float(value),
            bool: lambda value: value.lower() in ["true", "1"],
            dict: lambda value: eval(value),
            str: lambda value: value,
        }

    def get_collection_schema(self, database_name, table_name, sample_size=10):
        """Returns the schema of a table"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("Client not connected to MySQL.")
        query = f"DESCRIBE {database_name}.{table_name}"
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        schema = {}
        for row in cursor.fetchall():
            schema[row["Field"]] = row["Type"]
        return schema

    def execute_raw_query(self, query):
        """Executes a raw SQL query and returns the results."""
        if not self.connection or not self.connection.is_connected():
            raise Exception("Client not connected to MySQL.")

        try:
            # Create a cursor with dictionary=True to return rows as dictionaries
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)

            # Fetch all rows
            results = cursor.fetchall()

            # Close the cursor
            cursor.close()
            self.connection.commit()

            return results
        except Exception as e:
            # Raise a more descriptive error
            raise Exception(f"Error executing raw query: {e}")

    def get_syntax_highlighter(self):
        """Returns a syntax highlighter for the query editor"""
        return syntax_highlight(
            keywords=[
                "SELECT", "FROM", "WHERE", "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
                "INSERT", "INTO", "VALUES", "DELETE", "UPDATE", "SET",
                "CREATE", "TABLE", "DROP", "DATABASE", "USE", "SHOW", "DESCRIBE",
                "AND", "OR", "NOT", "IN", "LIKE", "IS", "NULL", "TRUE", "FALSE",
                "INNER", "OUTER", "LEFT", "RIGHT", "JOIN", "ON", "GROUP BY", "HAVING",
                "CASE", "WHEN", "THEN", "ELSE", "END", "AS", "DISTINCT", "UNION", "ALL",
                "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "AUTO_INCREMENT", "DEFAULT",
                "ADD", "COLUMN", "CONSTRAINT", "CHECK", "INDEX", "VIEW", "TRIGGER",
                "BEGIN", "END", "IF", "THEN", "ELSE", "ELSIF", "END IF", "LOOP", "END LOOP",
                "WHILE", "DO", "END WHILE", "FOR", "DECLARE", "CURSOR", "OPEN", "CLOSE",
                "COUNT", "SUM", "AVG", "MIN", "MAX", "AS", "IN", "OUT", "INOUT", "RETURN",
            ],
            operators=["=", ">", "<", ">=", "<=", "!=", "AND", "OR"],
            comment_line=["--"],
            comment_block=[{"/*": "*/"}],
            config={
                "keyword": {"foreground": "blue", "font": ("Courier", 10, "bold")},
                "string": {"foreground": "darkgreen"},
                "number": {"foreground": "purple"},
                "comment": {"foreground": "gray", "font": ("Courier", 10, "italic")},
                "operator": {"foreground": "red"},
            }
        )
