import tkinter as tk
from tkinter import ttk, messagebox
from business.config import Config

class ConnectionWindow:
    def __init__(self, root):
        self.root = root
        self.connection_string = None
        self.is_mock = False

        self.setup_ui()

    def setup_ui(self):
        """Creates the interface for entering the connection string."""
        self.root.title("Connect to MongoDB")

        # Label
        label = tk.Label(self.root, text="Insert or select the MongoDB connection string:")
        label.pack(pady=10)

        # Dropdown for saved connections
        self.connection_options = ttk.Combobox(
            self.root, 
            values = Config.get_instance().get_connections(), 
            width=50, 
            state="readonly"
        )
        self.connection_options.pack(pady=5, padx=10)
        self.connection_options.bind("<<ComboboxSelected>>", self.on_connection_selected)

        # Input field for new connection
        self.connection_entry = tk.Entry(self.root, width=50)
        self.connection_entry.insert(0, Config.get_instance().get_last_connection())  # Default value
        self.connection_entry.pack(pady=5, padx=10)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        connect_button = tk.Button(button_frame, text="Connect", command=self.connect)
        connect_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)

        mock_button = tk.Button(button_frame, text="Use Mock_data", command=self.mock)
        mock_button.pack(side=tk.LEFT, padx=5)

    def on_connection_selected(self, event):
        """Populate the entry field when a saved connection is selected."""
        selected_connection = self.connection_options.get()
        if selected_connection:
            self.connection_entry.delete(0, tk.END)
            self.connection_entry.insert(0, selected_connection)

    def connect(self):
        """Get the connection string and save it if valid, then close the window."""
        self.connection_string = self.connection_entry.get().strip()

        if not self.connection_string:
            messagebox.showerror("Error", "Connection string not provided")
        else:
            # Close the window after validation
            self.root.destroy()

    def cancel(self):
        """Close the window without saving the connection."""
        self.root.destroy()

    def mock(self):
        """Use mock data and close the window."""
        self.is_mock = True
        self.root.destroy()
