#!/usr/bin/env python3
"""Module to define the base class"""

import tkinter as tk
import tkinter.filedialog
import os
from PIL import Image, ImageTk
# from hashlib import md5


class TextEditorBase(tk.Tk):
    """Base class TextEditorBase defines basic setup for the GUI"""
    def __init__(self, *args, **kwargs):
        """Class construct"""
        super().__init__(*args, **kwargs)
        self.title('PyC Text Editor')
        self.geometry('800x500')
        self.resizable(1, 1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'PyC.png')

        icon = ImageTk.PhotoImage(Image.open(image_path))
        self.iconphoto(False, icon)

        self.text = tk.Text(self, font=('Times New Roman', 12), wrap="none")
        self.text.grid(row=0, column=0, sticky="nsew")

        # Vertical Scroll bar
        scrollbar_y = tk.Scrollbar(self, orient="vertical",
                                   command=self.text.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.text.configure(yscrollcommand=scrollbar_y.set)

        # Horizontal Scroll bar
        scrollbar_x = tk.Scrollbar(self, orient="horizontal",
                                   command=self.text.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.text.configure(xscrollcommand=scrollbar_x.set)


def run():
    """Run the windows"""
    root = TextEditorBase()
    root.mainloop()


if __name__ == "__main__":
    run()
