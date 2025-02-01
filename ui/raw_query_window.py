import tkinter as tk
import re
from tkinter import ttk, messagebox


class RawQueryWindow:
    def __init__(self, parent, manager):
        """Initialize the Raw Query Window."""
        self.parent = parent
        self.manager = manager
        self.window = tk.Toplevel(self.parent)
        self.window.title("Raw Query")
        self.window.geometry("800x600")

        # Fetch highlighting rules from the database client
        self.syntax_highlighter = manager.get_syntax_highlighter()

        if not self.syntax_highlighter:
            messagebox.showerror("Error", "Syntax Highlighter not found. or database client not supported.")
            self.window.destroy()
            return

        self.keywords = set(self.syntax_highlighter.get("keywords", []))
        self.operators = set(self.syntax_highlighter.get("operators", []))
        self.comment_markers = self.syntax_highlighter.get("comments", [])
        self.highlight_config = self.syntax_highlighter.get("config", {})

        self.setup_ui()

    def setup_ui(self):
        """Set up the UI components of the Raw Query Window."""
        # Top Section: Query Input
        top_frame = tk.Frame(self.window, bd=1, relief=tk.RAISED)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        query_label = tk.Label(top_frame, text="Enter Query:")
        query_label.pack(anchor="w", pady=5)

        # Frame for the Text widget with scrollbars
        query_input_frame = tk.Frame(top_frame)
        query_input_frame.pack(fill="both", expand=True)

        self.query_input = tk.Text(query_input_frame, height=10, wrap="word")
        self.query_input.pack(side=tk.LEFT, fill="both", expand=True)
        self.apply_syntax_highlighting()
        self.query_input.bind("<KeyRelease>", self.highlight_syntax)

        query_scroll_y = tk.Scrollbar(query_input_frame, orient="vertical", command=self.query_input.yview)
        query_scroll_y.pack(side=tk.RIGHT, fill="y")
        self.query_input.configure(yscrollcommand=query_scroll_y.set)

        query_scroll_x = tk.Scrollbar(top_frame, orient="horizontal", command=self.query_input.xview)
        query_scroll_x.pack(fill="x")
        self.query_input.configure(xscrollcommand=query_scroll_x.set)

        execute_button = tk.Button(
            top_frame,
            text="Execute",
            command=self.execute_query
        )
        execute_button.pack(anchor="e", pady=5)

        # Bottom Section: Query Results (Fixed)
        bottom_frame = tk.Frame(self.window, bd=1)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Wrapper frame for better scrollbar placement
        result_frame = tk.Frame(bottom_frame)
        result_frame.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(result_frame, orient="vertical")
        scroll_y.pack(side=tk.RIGHT, fill="y")

        scroll_x = ttk.Scrollbar(bottom_frame, orient="horizontal")
        scroll_x.pack(side=tk.BOTTOM, fill="x")

        self.result_table = ttk.Treeview(result_frame, show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.result_table.pack(side=tk.LEFT, fill="both", expand=True)

        # Link scrollbars correctly
        scroll_y.config(command=self.result_table.yview)
        scroll_x.config(command=self.result_table.xview)

    def execute_query(self):
        """Execute the selected query or the entire input if nothing is selected."""
        # Get selected text
        try:
            # Try to get the selected text
            query = self.query_input.selection_get().strip()
        except tk.TclError:
            # If no text is selected, use the entire input content
            query = self.query_input.get("1.0", tk.END).strip()

        if not query:
            messagebox.showerror("Error", "Query cannot be empty.")
            return

        try:
            # Clear previous results
            for item in self.result_table.get_children():
                self.result_table.delete(item)

            # Execute the query using the manager
            results = self.manager.execute_raw_query(query)

            if not results:
                messagebox.showinfo("Query Result", "Query executed successfully but returned no data.")
                return

            # Configure the table columns based on the results
            columns = list(results[0].keys())  # Assuming each result is a dictionary
            self.result_table["columns"] = columns

            for col in columns:
                self.result_table.heading(col, text=col)
                self.result_table.column(col, anchor="w", stretch=True)

            # Populate the table with data
            for row in results:
                values = [row[col] for col in columns]
                self.result_table.insert("", "end", values=values)

        except Exception as e:
            messagebox.showerror("Error", f"Error executing query: {e}")

    def apply_syntax_highlighting(self):
        """Apply syntax highlighting configuration from the database client."""
        for tag, config in self.highlight_config.items():
            self.query_input.tag_configure(tag, **config)

    def highlight_syntax(self, event=None):
        """Apply syntax highlighting dynamically."""
        text_content = self.query_input.get("1.0", tk.END)

        # Remove existing tags
        for tag in self.highlight_config.keys():
            self.query_input.tag_remove(tag, "1.0", tk.END)

        # Highlight connection client keywords
        for word in self.keywords:
            pattern = r"\b" + re.escape(word) + r"\b"
            for match in re.finditer(pattern, text_content, re.IGNORECASE):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.query_input.tag_add("keyword", start_idx, end_idx)

        # Highlight Strings (Single or Double Quotes)
        for match in re.finditer(r"('(?:''|[^'])*'|\"(?:\"\"|[^\"])*\")", text_content):
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.query_input.tag_add("string", start_idx, end_idx)

        # Highlight Numbers
        for match in re.finditer(r"\b\d+\b", text_content):
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.query_input.tag_add("number", start_idx, end_idx)

        # Highlight Operators
        for operator in self.operators:
            pattern = re.escape(operator)
            for match in re.finditer(pattern, text_content):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.query_input.tag_add("operator", start_idx, end_idx)

        # Highlight Comments (Line and Block)
        for marker in self.comment_markers.get("line", []):
            pattern = re.escape(marker) + r".*?$"
            for match in re.finditer(pattern, text_content, re.MULTILINE):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.query_input.tag_add("comment", start_idx, end_idx)

        for block in self.comment_markers.get("block", []):
            for start_marker, end_marker in block.items():
                pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
                for match in re.finditer(pattern, text_content, re.MULTILINE | re.DOTALL):
                    start_idx = f"1.0+{match.start()}c"
                    end_idx = f"1.0+{match.end()}c"
                    self.query_input.tag_add("comment", start_idx, end_idx)
