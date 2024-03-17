#!/usr/bin/env python3
"""Module to define the base class"""

import tkinter as tk
from tkinter import ttk


class TextEditorBase(ttk.Notebook):
    """Base class TextEditorBase defines basic setup for the GUI"""
    def __init__(self, *args, **kwargs):
        """Class construct"""
        super().__init__(*args, **kwargs)
        self.enable_traversal()
        self.pack(expand=1, fill="both")
        self.bind("<B1-Motion>", self.move_tab)
        #self.title("PyC Text Editor")
        #self.geometry("900x700")

    def current_tab(self):
        """Method to get the object of the current tab"""
        return self.nametowidget(self.select())

    def indexed_tab(self, index):
        return self.nametowidget(self.tabs()[index])

    def move_tab(self, event):
        """Check is there is more than one tab
            Use the y-coordinate of the current tab so that if the user
            moves the mouse up / down out of the range of the tabs,
            the left / right movement still moves the tab
        """
        if self.index("end") > 1:
            y = self.current_tab().winfo_y() - 5
            try:
                self.insert(min(event.widget.index('@%d,%d' % (event.x, y)),
                                self.index('end')-2), self.select())
            except tk.TclError:
                pass

    def run(self):
        """Run the windows"""
        self.mainloop()


if __name__ == "__main__":
    app = TextEditorBase()
    app.run()
