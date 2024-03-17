#!/usr/bin/env python3
"""Module to define the base class"""

import tkinter as tk
from tkinter import ttk
import os
from hashlib import md5


class TextEditorBase(ttk.Notebook):
    """Base class TextEditorBase defines basic setup for the GUI"""
    def __init__(self, *args, **kwargs):
        """Class construct"""
        super().__init__(*args, **kwargs)
        self.enable_traversal()
        self.pack(expand=1, fill="both")
        self.bind("<B1-Motion>", self.move_tab)
        # self.title("PyC Text Editor")
        # self.geometry("900x700")

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


class Tab(ttk.Frame):
    """Class Tab that defines Tab behaviour"""
    def __init__(self, *args, FileDir):
        """Class construct"""
        ttk.Frame.__init__(self, *args)
        self.textbox = self.create_text_widget()
        self.file_dir = None
        self.file_name = os.path.basename(FileDir)
        self.status = md5(self.textbox.get(1.0, 'end'.encode('utf-8')))

    def create_text_widget(self):
        """Handles the text widget"""
        # Horizontal Scroll bar
        xscrollbar = tk.Scrollbar(self, orient='horizontal')
        xscrollbar.pack(side='bottom', fill='x')

        # Vertical Scroll bar
        yscrollbar = tk.Scrollbar(self)
        yscrollbar.pack(side='right', fill='y')

        # Create Text Editor Box
        textbox = tk.Text(self, relief='sunken', borderwidth=0, wrap='none')
        textbox.config(xscrollcommand=xscrollbar.set,
                       yscrollcommand=yscrollbar.set, undo=True,
                       autoseparators=True)

        # Pack the textbox
        textbox.pack(fill='both', expand=True)

        # Configure Scrollbars
        xscrollbar.config(command=textbox.xview)
        yscrollbar.config(command=textbox.yview)

        return textbox


def run():
    """Run the windows"""
    root = tk.Tk()
    app = TextEditorBase()
    root.mainloop()


if __name__ == "__main__":
    run()
