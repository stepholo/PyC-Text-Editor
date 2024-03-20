#!/usr/bin/env python3
"""Module to define the base class"""

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import os
from PIL import Image, ImageTk
from hashlib import md5


class Tab(ttk.Frame):
    """Tab class to represent each tab in the text editor"""
    def __init__(self, *args, FileDir=None):
        ttk.Frame.__init__(self, *args)
        self.textbox = self.create_text_widget()
        self.file_dir = None
        if FileDir:
            self.file_dir = FileDir
            self.file_name = os.path.basename(FileDir)
        self.status = md5(self.textbox.get(1.0, 'end').encode('utf-8'))

    def create_text_widget(self):
        # Horizontal Scroll Bar
        xscrollbar = tk.Scrollbar(self, orient='horizontal')
        xscrollbar.pack(side='bottom', fill='x')

        # Vertical Scroll Bar
        yscrollbar = tk.Scrollbar(self)
        yscrollbar.pack(side='right', fill='y')

        # Create Text Editor Box
        textbox = tk.Text(self, font=('Times New Roman', 12), relief='sunken',
                          borderwidth=0, wrap='none')
        textbox.config(xscrollcommand=xscrollbar.set,
                       yscrollcommand=yscrollbar.set, undo=True,
                       autoseparators=True)

        # Pack the textbox
        textbox.pack(fill='both', expand=True)

        # Configure Scrollbars
        xscrollbar.config(command=textbox.xview)
        yscrollbar.config(command=textbox.yview)

        return textbox


class TextEditorBase(tk.Tk):
    """Base class TextEditorBase defines basic setup for the GUI"""
    def __init__(self, *args, **kwargs):
        """Class construct"""
        super().__init__(*args, **kwargs)
        self.title('PyC Text Editor')
        self.geometry('800x500')
        self.resizable(1, 1)

        # Notebook widget to manage multiple tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Add a default tab
        self.add_tab()

        # Find text editor icon directory and loads it
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'PyC.png')

        icon = ImageTk.PhotoImage(Image.open(image_path))
        self.iconphoto(False, icon)

    def add_tab(self):
        """Add a new tab to the Notebook"""
        tab = Tab(self.notebook)
        self.notebook.add(tab, text=f"Tab {self.notebook.index('end')}")


def run():
    """Run the windows"""
    root = TextEditorBase()
    root.mainloop()


if __name__ == "__main__":
    run()
