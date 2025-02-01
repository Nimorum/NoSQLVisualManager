import tkinter as tk
from tkinter import messagebox
import bson

class AddRowPanel:
    def __init__(self, root, data_types):
        """Initialize the add row panel."""
        self.data_types = data_types
        self.result = None  # Will store the new document
        self.window = tk.Toplevel(root)
        self.window.title("Add Document")
        self.window.geometry("300x400")
        self.window.grab_set()  # Prevent interaction with the main window

        # Create input fields dynamically based on data types
        self.inputs = {}
        row = 0
        for field, dtype in self.data_types.items():
            label = tk.Label(self.window, text=field)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(self.window)
            if dtype == bson.objectid.ObjectId:
                entry.insert(0, bson.objectid.ObjectId())
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="e")
            self.inputs[field] = (entry, dtype)
            row += 1

        # Button frame
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        # Save Button
        save_button = tk.Button(button_frame, text="Save", command=self.save)
        save_button.pack(side=tk.LEFT, padx=10)

        # Cancel Button
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=10)

    def save(self):
        """Validate inputs and save the document."""
        try:
            new_document = {}
            for field, (entry, dtype) in self.inputs.items():
                value = entry.get()  # Raw string input from the field
                new_document[field] = value
            self.result = new_document
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Validation Error", f"Invalid input for field '{field}': {e}")

    def cancel(self):
        """Cancel the operation."""
        self.result = None
        self.window.destroy()

    def show(self):
        """Display the panel and return the result."""
        self.window.wait_window()  # Wait until the window is closed
        return self.result