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
        self.status = md5(self.textbox.get(1.0, 'end').encode('utf-8'))

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


class Editor:
    def __init__(self, master):
        self.master = master
        self.master.title("PyC Text Editor")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.filetypes = (("Normal text file", "*.txt"), ("all files", "*.*"))
        self.init_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.untitled_count = 1

        # Create Notebook ( for tabs ).
        self.nb = ttk.Notebook(master)
        self.nb.bind("<Button-2>", self.close_tab)
        self.nb.bind('<<NotebookTabChanged>>', self.tab_change)
        self.nb.bind('<Button-3>', self.right_click_tab)

        # Override the X button.
        self.master.protocol('WM_DELETE_WINDOW', self.exit)

        # Create Menu Bar
        menubar = tk.Menu(self.master)

        # Create File Menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file)
        # filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        # filemenu.add_command(label="Save As...", command=self.save_as)
        filemenu.add_command(label="Close", command=self.close_tab)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)

        # Create Edit Menu
        '''editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.undo)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.cut)
        editmenu.add_command(label="Copy", command=self.copy)
        editmenu.add_command(label="Paste", command=self.paste)
        editmenu.add_command(label="Delete", command=self.delete)
        editmenu.add_command(label="Select All", command=self.select_all)'''

        # Create Format Menu, with a check button for word wrap.
        formatmenu = tk.Menu(menubar, tearoff=0)
        self.word_wrap = tk.BooleanVar()
        formatmenu.add_checkbutton(label="Word Wrap",
                                   onvalue=True, offvalue=False,
                                   variable=self.word_wrap, command=self.wrap)

        # Attach to Menu Bar
        menubar.add_cascade(label="File", menu=filemenu)
        # menubar.add_cascade(label="Edit", menu=editmenu)
        menubar.add_cascade(label="Format", menu=formatmenu)
        self.master.config(menu=menubar)

        # Create right-click menu.
        '''self.right_click_menu = tk.Menu(self.master, tearoff=0)
        self.right_click_menu.add_command(label="Undo", command=self.undo)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Cut", command=self.cut)
        self.right_click_menu.add_command(label="Copy", command=self.copy)
        self.right_click_menu.add_command(label="Paste", command=self.paste)
        self.right_click_menu.add_command(label="Delete", command=self.delete)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Select All",
                                          command=self.select_all)'''

        # Create tab right-click menu
        self.tab_right_click_menu = tk.Menu(self.nb, tearoff=0)
        self.tab_right_click_menu.add_command(label="New Tab",
                                              command=self.new_file)

        # Keyboard / Click Bindings
        self.master.bind_class('Text', '<Control-s>', self.save_file)
        # self.master.bind_class('Text', '<Control-o>', self.open_file)
        self.master.bind_class('Text', '<Control-n>', self.new_file)
        # self.master.bind_class('Text', '<Control-a>', self.select_all)
        self.master.bind_class('Text', '<Control-w>', self.close_tab)
        # self.master.bind_class('Text', '<Button-3>', self.right_click)

        # Create initial tab and 'Add' tab
        self.nb.add(Tab(FileDir='Untitled'), text='Untitled')
        self.nb.add(Tab(FileDir='f'), text=' + ')

    def wrap(self):
        if self.word_wrap.get() is True:
            for i in range(self.nb.index('end')-1):
                self.nb.indexed_tab(i).textbox.config(wrap="word")
        else:
            for i in range(self.nb.index('end')-1):
                self.nb.indexed_tab(i).textbox.config(wrap="none")

    def close_tab(self, event=None):
        """Close the tab corresponding to the event position."""
        if event is None or event.type == str(2):
            selected_tab = self.nb.current_tab()
        else:
            try:
                index = event.widget.index('@%d,%d' % (event.x, event.y))
                selected_tab = self.nb.indexed_tab(index)
                if index == self.nb.index('end')-1:
                    return False
            except tk.TclError:
                return False

        # Prompt to save changes before closing tab
        if self.save_changes(selected_tab):
            check = self.nb.tabs()[-2]
            if self.nb.index('current') > 0 and self.nb.select() == check:
                self.nb.select(self.nb.index('current')-1)
            self.nb.forget(selected_tab)
        else:
            return False

        # Exit if last tab is closed
        if self.nb.index("end") <= 1:
            self.master.destroy()

        return True

    def exit(self):
        """Check if any changes have been made"""
        for i in range(self.nb.index('end')-1):
            if self.close_tab() is False:
                break

    def tab_change(self, event):
        """Handle tab change event."""
        if self.nb.select() == self.nb.tabs()[-1]:
            self.new_file()

    def right_click_tab(self, event):
        """Handle right click on tab event."""
        self.tab_right_click_menu.post(event.x_root, event.y_root)

    def new_file(self, *args):
        # Create new tab
        new_tab = Tab(FileDir=self.default_filename())
        new_tab.textbox.config(wrap='word' if self.word_wrap.get() else 'none')
        self.nb.insert(self.nb.index('end')-1, new_tab, text=new_tab.file_name)
        self.nb.select(new_tab)

    def save_file(self, *args):
        cur_tab = self.nb.current_tab()
        # If file directory is empty or Untitled, use save_as to get save
        # information from user.
        if not cur_tab.file_dir:
            return self.save_as()
        # Otherwise save file to directory, overwriting existing file
        # or creating a new one.
        else:
            with open(cur_tab.file_dir, 'w') as file:
                file.write(cur_tab.textbox.get(1.0, 'end'))
            # Update hash
            cur_tab.status = md5(cur_tab.textbox.get(
                1.0, 'end').encode('utf-8'))

            return True


def run():
    """Run the windows"""
    root = tk.Tk()
    app = Editor(root)
    root.mainloop()


if __name__ == "__main__":
    run()
