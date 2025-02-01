import tkinter as tk
from tkinter import ttk, messagebox
from ui.add_row_panel import AddRowPanel
from ui.confirmation_window import ConfirmationWindow
from ui.raw_query_window import RawQueryWindow


class MainWindow:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.current_path = "root"  # Initial path in the toolbar
        self.selected_db = None
        self.selected_collection = None
        self.selected_document = None
        self.documents = []
        self.data_types = {}
        self.query_field = None
        self.take_field = None
        self.skip_field = None
        self.sort_order = -1

        self.setup_ui()

    def setup_ui(self):
        """Configure the main interface"""
        self.root.title("NoSQL Visual Manager")
        self.root.geometry("900x600")

        # Toolbar (Top)
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.path_label = tk.Label(self.toolbar, text=f"Path: {self.current_path}")
        self.path_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        add_button = tk.Button(self.toolbar, text="Add Document", command=self.add_row)
        add_button.pack(side=tk.RIGHT, padx=10, pady=5)
        delete_button = tk.Button(self.toolbar, text="Delete Row", command=self.delete_row)
        delete_button.pack(side=tk.RIGHT, padx=10, pady=5)
        raw_query_button = tk.Button(self.toolbar, text="Raw Query", command=self.open_raw_query_window)
        raw_query_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Utility Section (Below Toolbar)
        self.utility_section = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.utility_section.pack(side=tk.TOP, fill=tk.X)

        # Left Utility Section
        self.left_utility = tk.Frame(self.utility_section, width=200)
        self.left_utility.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Right Utility Section
        self.right_utility = tk.Frame(self.utility_section)
        self.right_utility.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        tk.Button(
            self.right_utility,
            text=">>",
            command=lambda: self.search(
                query=self.query_field.get(),
                skip=self.skip_field.get(),
                take=self.take_field.get()
            )
        ).pack(side=tk.RIGHT, padx=2)
        self.take_field = tk.Entry(self.right_utility, width=5)
        self.take_field.pack(side=tk.RIGHT, padx=2)
        self.take_field.insert(0, "100")
        tk.Label(self.right_utility, text="take:").pack(side=tk.RIGHT, padx=2)
        self.skip_field = tk.Entry(self.right_utility, width=5)
        self.skip_field.pack(side=tk.RIGHT, padx=2)
        self.skip_field.insert(0, "0")
        tk.Label(self.right_utility, text="skip:").pack(side=tk.RIGHT, padx=2)
        self.query_field = tk.Entry(self.right_utility)
        self.query_field.pack(side=tk.RIGHT, padx=2, expand=True, fill=tk.X)
        tk.Label(self.right_utility, text="filter:").pack(side=tk.RIGHT, padx=2)

        # Sidebar (Left)
        self.sidebar = tk.Frame(self.root, width=200, bd=1, relief=tk.SUNKEN)
        self.tree = ttk.Treeview(self.sidebar)
        self.tree.heading("#0", text="Data Bases", anchor=tk.W)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)  # Event on selecting in the tree
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Main View (Center)
        self.main_view = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        self.main_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure TreeView
        self.data_table = ttk.Treeview(self.main_view, show="headings")
        self.data_table.grid(row=0, column=0, sticky="nsew")

        # Add scroll bars
        scroll_y = ttk.Scrollbar(self.main_view, orient="vertical", command=self.data_table.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x = ttk.Scrollbar(self.main_view, orient="horizontal", command=self.data_table.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.data_table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.data_table.bind("<Double-1>", self.on_cell_double_click)

        # Configure TreeView and scroll bars expansion
        self.main_view.grid_rowconfigure(0, weight=1)  # Allow TreeView to expand vertically
        self.main_view.grid_columnconfigure(0, weight=1)  # Allow TreeView to expand horizontally

        # Fill the tree with databases
        self.populate_tree()

    def populate_tree(self):
        """Fill the tree with databases and collections"""
        try:
            databases = self.manager.get_databases()
            for db in databases:
                db_node = self.tree.insert("", "end", text=db, open=False)
                collections = self.manager.get_collections(db)
                for collection in collections:
                    self.tree.insert(db_node, "end", text=collection)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading databases: {e}")

    def on_tree_select(self, event):
        """Handle tree selection"""
        selected_item = self.tree.selection()[0]  # Get the selected item
        item_text = self.tree.item(selected_item, "text")  # Item text

        # Check if the item is a collection (has a parent)
        parent = self.tree.parent(selected_item)
        if parent:
            self.selected_db = self.tree.item(parent, "text")
            self.selected_collection = item_text
            self.current_path = f"root > {self.selected_db} > {self.selected_collection}"
            self.path_label.config(text=f"Path: {self.current_path}")
            self.search(query=None, skip=0, take=10)
        else:
            self.selected_db = item_text
            self.selected_collection = None
            self.current_path = f"root > {self.selected_db}"
            self.path_label.config(text=f"Path: {self.current_path}")

    def populate_data_table(self):
        """Load the selected collection data into the main table"""
        try:
            if not self.selected_db or not self.selected_collection:
                return
            
            self.selected_document = None

            # Clear old columns and data
            self.data_table.delete(*self.data_table.get_children())
            self.data_table["columns"] = []

            if self.documents:
                # Configure columns dynamically from the first document's keys
                columns = list(self.documents[0].keys())  # Get document keys
                self.data_table["columns"] = columns

                # Configure headers and columns
                for col in columns:
                    self.data_table.heading(col, text=col, command=lambda c=col: self.sort_column(c))
                    self.data_table.column(col, anchor="w", stretch=True)

                # Insert data into the table
                for doc in self.documents:
                    row = [str(doc[col]) for col in columns]
                    self.data_table.insert("", "end", values=row)

            # Force table update
            self.data_table.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error", f"Error: loading data: {e}")

    def add_row(self):
        """Open a panel to add a new row to the collection."""
        if not self.selected_collection:
            messagebox.showerror("Error", "Select a collection first")
            return

        # Data types for the current collection (replace with actual logic)
        first_document = self.documents[0]
        data_types = {key: type(value) for key, value in first_document.items()}

        # Open the AddRowPanel
        add_panel = AddRowPanel(self.root, data_types)
        new_document = add_panel.show()

        if new_document:
            try:
                # Insert the new document into the database
                self.manager.insert_document(self.selected_db, self.selected_collection, new_document)
                self.search()  # Refresh the table
            except Exception as e:
                messagebox.showerror("Error", f"Error adding document: {e}")

    def delete_row(self):
        selected_item = self.data_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Select a row first")
            return
        
        confirm_dialog = ConfirmationWindow(self.root, "Are you sure you want to delete this row?")
        if not confirm_dialog.show():
            return  # If user cancels, do nothing
        
        try:
            row_index = self.data_table.index(selected_item)
            document = self.documents[row_index]

            self.manager.delete_document(self.selected_db, self.selected_collection, document)
            self.search()  # Refresh the table
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting document: {e}")

    def on_cell_double_click(self, event):
        """Handle double-click event on a table cell for editing"""
        # Identify the row and column
        row_id = self.data_table.identify_row(event.y)
        col_id = self.data_table.identify_column(event.x)

        if not row_id or not col_id.startswith("#"):
            return  # Ignore if not a valid cell

        # Get row index and column name
        row_index = self.data_table.index(row_id)
        column_index = int(col_id[1:]) - 1
        column_name = self.data_table["columns"][column_index]

        # Get the current value
        current_value = self.data_table.item(row_id, "values")[column_index]

        # Calculate the geometry of the cell
        bbox = self.data_table.bbox(row_id, col_id)
        if not bbox:
            return

        x, y, width, height = bbox

        # Create an entry widget in place of the cell
        entry = tk.Entry(self.data_table)
        entry.insert(0, current_value)
        entry.select_range(0, tk.END)
        entry.focus()

        # Place the entry widget over the cell
        entry.place(x=x, y=y, width=width, height=height)

        def save_edit(event=None):
            new_value = entry.get()

            confirm = ConfirmationWindow(self.root, f"Do you want to change the '{column_name}' field to '{new_value}'?")
            if not confirm.show():
                self.search()  # Refresh the table
                return  # If user cancels, do nothing
            entry.destroy()  # Remove the entry widget
            # Update the local document and database
            document = self.documents[row_index]
            if column_name in document:
                document[column_name] = new_value
                try:
                    self.manager.update_document(self.selected_db, self.selected_collection, document, column_name)
                    self.search()  # Refresh the table
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating document: {e}")

        def cancel_edit(event=None):
            entry.destroy()  # Remove the entry widget without saving

        # Bind save and cancel events
        entry.bind("<Return>", save_edit)
        entry.bind("<Escape>", cancel_edit)
    
    def sort_column(self, column):
        """Sort the data by the selected column."""
        if not self.documents:
            return
        self.sort_order = -1 * self.sort_order
        self.search(order_by=column, sort_order=self.sort_order, query=self.query_field.get(), skip=self.skip_field.get(), take=self.take_field.get())

    def search(self, order_by=None, sort_order=1, query=None, skip=0, take=100):
        """Search for documents in the current collection."""
        if not self.selected_db or not self.selected_collection:
            return
        skip = int(skip)
        take = int(take)
        if query == "":
            query = None

        try:
            self.documents = self.manager.fetch_documents(self.selected_db, self.selected_collection, order_by, sort_order, query, take, skip)
            self.populate_data_table()
        except Exception as e:
            messagebox.showerror("Error", f"Error searching documents: {e}")

    def open_raw_query_window(self):
        """Opens the Raw Query Window."""
        RawQueryWindow(self.root, self.manager)