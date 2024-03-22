#!/usr/bin/env python3
"""Module to define functions used for Menu options"""

from tkinter import filedialog
import tkinter as tk


def create_menu(root, editor):
    menubar = tk.Menu(root)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New tab    Ctrl+N",
                          command=lambda: new_file(editor))
    file_menu.add_command(label="Open         Ctrl+O",
                          command=lambda: open_file(editor))
    file_menu.add_command(label="Save          Ctrl+S",
                          command=lambda: save_file(editor))
    file_menu.add_command(label="Save As      Ctrl+Shift+S",
                          command=lambda: save_as(editor))
    file_menu.add_command(label="Save All     Ctrl+A",
                          command=lambda: save_all(editor))
    file_menu.add_separator()
    file_menu.add_command(label="Close tab  Ctrl+W",
                          command=lambda: close_tab(editor))
    file_menu.add_command(label="Close Window   Ctrl+Shift+W",
                          command=lambda: close_window(root))
    file_menu.add_separator()
    file_menu.add_command(label="Exit   Ctrl+Q",
                          command=lambda: exit_editor(root))
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    # Edit Menu
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(
        label="Undo     Ctrl+Z",
        command=lambda: editor.current_tab().textbox.edit_undo(),
        state='normal'
        )
    editmenu.add_separator()
    editmenu.add_command(
        label="Copy     Ctrl+C",
        command=lambda:
        editor.current_tab().textbox.event_generate("<<Copy>>"),
        state='disabled'
        )
    editmenu.add_command(
        label="Cut       Ctrl+X",
        command=lambda: editor.current_tab().textbox.event_generate("<<Cut>>"),
        state='disabled'
    )
    editmenu.add_command(
        label="Paste    Ctrl+V",
        command=lambda:
        editor.current_tab().textbox.event_generate("<<Paste>>"),
        state='normal'
        )
    editmenu.add_command(
        label="Delete   Del",
        command=lambda:
        editor.current_tab().textbox.delete(tk.SEL_FIRST, tk.SEL_LAST),
        state='disabled'
        )
    menubar.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menubar)

    # Bind text Selection event to update menu state
    editor.current_tab().textbox.bind("<<Selection>>",
                                      lambda event:
                                      update_edit_menu_state(editor, editmenu)
                                      )

    # File Menu Keyboard bindings
    root.bind_all("<Control-n>", lambda event: new_file(editor))
    root.bind_all("<Control-o>", lambda event: open_file(editor))
    root.bind_all("<Control-s>", lambda event: save_file(editor))
    root.bind_all("<Control-Shift-S>", lambda event:
                  save_as(editor))
    root.bind_all("<Control-a>", lambda event: save_all(editor))
    root.bind_all("<Control-w>", lambda event: close_tab(editor))
    root.bind_all("<Control-Shift-W>", lambda event: close_window(editor))
    root.bind_all("<Control-q>", lambda event: exit_editor(root))


def close_window(root):
    root.destroy()


def new_file(editor):
    editor.add_tab()


def open_file(editor):
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        tab = editor.current_tab()
        tab.textbox.delete('1.0', tk.END)
        tab.textbox.insert('1.0', content)


def save_file(editor):
    tab = editor.current_tab()
    if tab.file_dir:
        content = tab.textbox.get('1.0', tk.END)
        with open(tab.file_dir, 'w') as file:
            file.write(content)
    else:
        save_as(editor)


def save_as(editor):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        tab = editor.current_tab()
        content = tab.textbox.get('1.0', tk.END)
        with open(file_path, 'w') as file:
            file.write(content)


def save_all(editor):
    for tab_id in editor.tabs():
        tab = editor.nametowidget(tab_id)
        if tab.file_dir:
            content = tab.textbox.get('1.0', tk.END)
            with open(tab.file_dir, 'w') as file:
                file.write(content)
        else:
            save_as(editor)


def close_tab(editor):
    current_index = editor.index(editor.select())
    if current_index != 0:
        editor.forget(current_index)
    else:
        exit_editor(editor)


def exit_editor(root):
    root.quit()


def update_edit_menu_state(editor, editmenu):
    """Update state of Copy, Cut, and Delete menu items
       based on text selection
    """
    if editor.current_tab().textbox.tag_ranges(tk.SEL):
        editmenu.entryconfig(2, state='normal')  # Index 2 corresponds to Copy
        editmenu.entryconfig(3, state='normal')  # Index 3 corresponds to Cut
        editmenu.entryconfig(5, state='normal')  # Index 5 corr to Delete
    else:
        editmenu.entryconfig(2, state='disabled')  # Index 2 corr to Copy
        editmenu.entryconfig(3, state='disabled')  # Index 3 corresponds to Cut
        editmenu.entryconfig(5, state='disabled')  # Index 5 corr to Delete
