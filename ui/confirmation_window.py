import tkinter as tk
class ConfirmationWindow:
    def __init__(self, root, message):
        """Initialize the confirmation window."""
        self.result = False  # Default result is False
        self.window = tk.Toplevel(root)
        self.window.title("Confirm Action")
        self.window.geometry("300x150")
        self.window.grab_set()  # Block interaction with the main window

        # Add a message
        label = tk.Label(self.window, text=message, wraplength=250)
        label.pack(pady=20)

        # Button frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        # OK Button
        ok_button = tk.Button(button_frame, text="OK", command=self.confirm)
        ok_button.pack(side=tk.LEFT, padx=10)

        # Cancel Button
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=10)

    def confirm(self):
        """Set result to True and close the window."""
        self.result = True
        self.window.destroy()

    def cancel(self):
        """Set result to False and close the window."""
        self.result = False
        self.window.destroy()

    def show(self):
        """Run the window and return the result."""
        self.window.wait_window()  # Wait until the window is closed
        return self.result