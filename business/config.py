import json
import os

class Config:
    _instance = None  # Static variable to hold the singleton instance

    def __new__(cls, config_file="config.json"):
        """
        Create or return the singleton instance of ConfigClass.
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_file="config.json"):
        """
        Initialize the ConfigClass with a specified configuration file.
        Ensures that the file is loaded only once.
        """
        if not self._initialized:
            self.config_file = config_file
            self._data = {}
            self._ensure_file_exists()
            self._load_config()
            self._initialized = True
        else:
            raise Exception("Config class is a singleton. Use Config.get_instance() to get the instance.")

    @staticmethod
    def get_instance():
        """
        Get the singleton instance of the Config class.
        
        Returns:
            Config: The singleton instance of the Config class.
        """
        return Config._instance

    def _ensure_file_exists(self):
        """Ensure the configuration file exists, and create it if it doesn't."""
        if not os.path.exists(self.config_file):
            default_config = {
                "connections": [],
                "app_settings": {},  # Example for other configurations
                "last_connection_used": "mongodb://localhost:27017",  # Example: Last used connection string
                "last_checked_for_updates": None,  # TODO: Example for update checks
            }
            with open(self.config_file, "w") as file:
                json.dump(default_config, file, indent=4)

    def _load_config(self):
        """Load the connections from the JSON configuration file."""
        with open(self.config_file, "r") as file:
            self._data = json.load(file)

    def _save_config(self):
        """Save the connections back to the JSON configuration file."""
        with open(self.config_file, "w") as file:
            json.dump(self._data, file, indent=4)

    def get_connections(self):
        """
        Get the list of saved connections.
        
        Returns:
            list: A list of saved connection strings.
        """
        return self._instance._data.get("connections", [])
    
    def get_last_connection(self):
        """
        Get the last used connections.
        
        Returns:
            str: last connection used.
        """
        return self._instance._data.get("last_connection_used", "")
    
    def set_last_connection(self,connection_string):
        """
        Set the last connection string used.
        
        Args:
            connection_string (str): The connection string to set as last used.
        """
        if connection_string != self._instance._data["last_connection_used"]:
            self._instance._data["last_connection_used"] = connection_string
            self._instance._save_config()

    def add_connection(self,connection_string):
        """
        Add a new connection string to the configuration.
        
        Args:
            connection_string (str): The connection string to add.
        """
        if connection_string not in self._instance._data["connections"]:
            self._instance._data["connections"].append(connection_string)
            self._instance._save_config()

    def remove_connection(self,connection_string):
        """
        Remove a connection string from the configuration.
        
        Args:
            connection_string (str): The connection string to remove.
        """
        if connection_string in self._data["connections"]:
            self._instance._data["connections"].remove(connection_string)
            self._instance._save_config()