#!/usr/bin/env python3
"""Module to define the base class"""

import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from hashlib import md5
from menu_file import create_menu
import subprocess
import json


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

    def get_file_path(self):
        return self.file_dir

    def explain_with_chatgpt(self, editor):
        """Function that takes file content as chatgpt prompt and
        appends the response to the text file
        """
        # Get the path of the currently open file in the editor
        file_path = editor.current_tab().get_file_path()

        # Ensure the file path is not None
        if file_path is None:
            print("No file is open.")
            return

        # Read the content of the file
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Prepare data to send to Node.js script
        data = {
            'fileContent': file_content,
            'filePath': file_path
            }

        # Execute the Node.js script passing the file content and file path
        # as arguments
        path = r"C:\Users\LENOVO\Desktop\PyC-Text-Editor-1\gpt-api\chatgpt.js"
        process = subprocess.Popen(['node', path, file_content, file_path],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE
                                   )

        # Send data to the Node.js script
        process.stdin.write(json.dumps(data).encode())
        process.stdin.close()

        # Get the response from the Node.js script
        stdout, stderr = process.communicate()

        # Check if there was an error in executing the Node.js script
        if stderr:
            print("Error executing Node.js script:", stderr.decode())
            return None

        # Process the response from Node.js if needed
        response_data = stdout.decode().strip()
        print(response_data)


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
        # Create initial tab with text 'Untitled'
        initial_tab = Tab(self, FileDir='Untitled')
        self.add(initial_tab, text='Untitled')

        # Create 'Add' tab with text '+'
        add_tab = Tab(self, FileDir='f')
        self.add(add_tab, text=' + ')


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
