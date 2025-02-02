class syntax_highlight:

    def __init__(self, keywords: list, operators: list, comment_line: list, comment_block: list, config: dict):
        """
        Initializes the repository with a client (MongoDBClient, MockClient, etc.)
        and the selected database name.
        """
        self.keywords = keywords
        self.operators = operators
        self.comments = {"line": comment_line, "block": comment_block}
        self.config = config
