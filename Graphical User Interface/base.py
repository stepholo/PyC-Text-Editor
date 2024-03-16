#!/usr/bin/env python3
"""Module to define the base class"""

import tkinter as tk


class TextEditorBase(tk.Tk):
    """Base class TextEditorBase defines basic setup for the GUI"""
    def __init__(self, *args, **kwargs):
        """Class construct"""
        super().__init__(*args, **kwargs)
        self.title("PyC Text Editor")
        self.geometry("900x700")

        self.setup_ui()

    def setup_ui(self):
        """Method to define widgets and setup layout"""
        pass

    def run(self):
        """Run the windows"""
        self.mainloop()


if __name__ == "__main__":
    app = TextEditorBase()
    app.run()
