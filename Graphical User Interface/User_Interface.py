#!/usr/bin/env python3
"""Module to define the base class"""

import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from hashlib import md5
import menu_option


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


class TextEditorBase(ttk.Notebook):
    """Base class TextEditorBase defines basic setup for the GUI"""
    def __init__(self, *args, **kwargs):
        """Class construct"""
        super().__init__(*args, **kwargs)

        # Add a default tab
        self.add_tab()

        # Find text editor icon directory and loads it
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'PyC.png')

        icon = ImageTk.PhotoImage(Image.open(image_path))
        self.master.iconphoto(False, icon)

        self.enable_traversal()
        self.bind("<B1-Motion>", self.move_tab)

        # File types for file dialogs
        self.filetypes = (("Normal text file", "*.txt"), ("all files", "*.*"))

        # Initial directory for file dialogs
        self.init_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Counter for untitled files
        self.untitled_count = 1

    # Get the object of the current tab
    def current_tab(self):
        return self.nametowidget(self.select())

    def indexed_tab(self, index):
        return self.nametowidget(self.tabs()[index])

    # Move tab position by dragging tab
    def move_tab(self, event):
        """Check if there is more than one tab
            Use the y-coordinate of the current tab so that if the user
            moves the mouse up / down out of the range of the tabs,
            the left / right movement still moves the tab.
        """
        if self.index("end") > 1:
            y = self.current_tab().winfo_y() - 5
            try:
                self.insert(min(event.widget.index('@%d,%d' % (event.x, y)),
                                self.index('end') - 2), self.select())
            except tk.TclError:
                pass

    def add_tab(self):
        """Add a new tab to the Notebook"""
        tab = Tab(self)
        self.add(tab, text=f"Tab {self.index('end')}")


def create_menu(root, editor):
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New tab    Ctrl+N",
                          command=lambda: menu_option.new_file(editor))
    file_menu.add_command(label="Open         Ctrl+O",
                          command=lambda: menu_option.open_file(editor))
    file_menu.add_command(label="Save          Ctrl+S",
                          command=lambda: menu_option.save_file(editor))
    file_menu.add_command(label="Save As      Ctrl+Shift+S",
                          command=lambda: menu_option.save_as(editor))
    file_menu.add_command(label="Save All     Ctrl+A",
                          command=lambda: menu_option.save_all(editor))
    file_menu.add_separator()
    file_menu.add_command(label="Close tab  Ctrl+W",
                          command=lambda: menu_option.close_tab(editor))
    file_menu.add_command(label="Close Window   Ctrl+Shift+W",
                          command=lambda: close_window(root))
    file_menu.add_separator()
    file_menu.add_command(label="Exit   Ctrl+Q",
                          command=lambda: menu_option.exit_editor(root))
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    # Keyboard bindings
    root.bind_all("<Control-n>", lambda event: menu_option.new_file(editor))
    root.bind_all("<Control-o>", lambda event: menu_option.open_file(editor))
    root.bind_all("<Control-s>", lambda event: menu_option.save_file(editor))
    root.bind_all("<Control-Shift-S>", lambda event:
                  menu_option.save_as(editor))
    root.bind_all("<Control-a>", lambda event: menu_option.save_all(editor))
    root.bind_all("<Control-w>", lambda event: menu_option.close_tab(editor))
    root.bind_all("<Control-Shift-W>", lambda event: close_window(editor))
    root.bind_all("<Control-q>", lambda event: menu_option.exit_editor(root))


def close_window(root):
    root.destroy()


def run():
    """Run the windows"""
    root = tk.Tk()
    root.title('PyC Text Editor')
    root.geometry('800x500')
    root.resizable(1, 1)

    # Notebook widget to manage multiple tabs
    editor = TextEditorBase(root)
    editor.pack(fill="both", expand=True)

    create_menu(root, editor)

    root.mainloop()


if __name__ == "__main__":
    run()
