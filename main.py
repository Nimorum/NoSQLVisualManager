import tkinter as tk
from tkinter import messagebox
from business.config import Config
from db.mock_client import MockClient
from db.mongodb_client import MongoDBClient
from db.mySql_client import MySQLClient
from db.repository import Repository
from ui.connection_window import ConnectionWindow
from business.business_manager import BusinessManager
from ui.main_window import MainWindow


def main():
    # Load the configuration file
    Config("config.json")
    # Create the window for the connection string
    connection_root = tk.Tk()
    connection_window = ConnectionWindow(connection_root)
    connection_root.mainloop()
    # Get the connection string entered by the user
    connection_string = connection_window.connection_string
    is_mock = connection_window.is_mock

    if not connection_string and not is_mock:
        raise Exception("No connection string provided")

    try:
        # Create the database client
        if is_mock:
            client = MockClient("")
        else:
            if connection_string.startswith("mongodb"):
                client = MongoDBClient(connection_string)
            elif connection_string.startswith("mysql"):
                client = MySQLClient(connection_string)
            else:
                raise Exception("Invalid connection string")

        repository = Repository(client, None)
        manager = BusinessManager(repository)
        manager.connect()

        # Start the main interface
        main_root = tk.Tk()
        MainWindow(main_root, manager)  # Pass the manager to the main UI
        main_root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    main()
