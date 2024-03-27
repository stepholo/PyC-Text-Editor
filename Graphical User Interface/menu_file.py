#!/usr/bin/env python3
"""Module to define functions used for Menu options"""

from tkinter import filedialog
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import ttk
import os


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
    editmenu.add_separator()
    editmenu.add_command(
        label="Explain with chatGPT",
        command=lambda:
        editor.current_tab().explain_with_chatgpt(editor)
    )
    menubar.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menubar)

    # Bind text Selection event to update menu state
    editor.current_tab().textbox.bind("<<Selection>>",
                                      lambda event:
                                      update_edit_menu_state(editor, editmenu)
                                      )

    # View Menu
    viewmenu = tk.Menu(menubar, tearoff=0)
    viewmenu.add_checkbutton(label="Status Bar",
                             command=lambda: toggle_status_bar(editor))
    viewmenu.add_checkbutton(label="Word Wrap",
                             command=lambda: toggle_word_wrap(editor))
    menubar.add_cascade(label="View", menu=viewmenu)

    # Bind cursor movement event
    editor.current_tab().textbox.bind(
        "<Motion>", lambda event: update_status_bar(editor, editor.status_bar)
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
        # Update tab name to reflect the file name
        tab.file_dir = file_path
        tab.file_name = os.path.basename(file_path)
        editor.tab(editor.select(), text=tab.file_name)


def save_file(editor):
    tab = editor.current_tab()
    if tab.file_dir:  # Check if file_dir is set (file has been saved before)
        content = tab.textbox.get('1.0', tk.END)
        with open(tab.file_dir, 'w') as file:
            file.write(content)
    else:  # File is being saved for the first time
        if tab.file_name == 'Untitled' or tab.file_name is None:
            save_as(editor)
        else:
            # File has been renamed, save without opening file dialog
            file_path = os.path.join(
                os.path.dirname(tab.file_dir), tab.file_name
                )
            content = tab.textbox.get('1.0', tk.END)
            with open(file_path, 'w') as file:
                file.write(content)
            tab.file_dir = file_path  # Update file_dir with the new path
            editor.tab(editor.select(), text=tab.file_name)  # Update tab name


def save_as(editor):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        tab = editor.current_tab()
        content = tab.textbox.get('1.0', tk.END)
        with open(file_path, 'w') as file:
            file.write(content)
        # Update tab attributes with new file information
        tab.file_dir = file_path
        tab.file_name = os.path.basename(file_path)
        editor.tab(editor.select(), text=tab.file_name)


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
    current_tab = editor.current_tab()
    if has_unsaved_changes(current_tab):
        confirm_close = messagebox.askyesno(
            "Unsaved Changes, "
            "There are unsaved changes. "
            "Do you want to save before closing?"
            )
        if confirm_close:
            save_file(editor)
        else:
            editor.forget(editor.select())
    else:
        editor.forget(editor.select())


def exit_editor(root):
    current_tab = root.current_tab()
    if has_unsaved_changes(current_tab):
        confirm_close = messagebox.askyesno(
            "Unsaved Changes, "
            "There are unsaved changes. "
            "Do you want to save before exiting?"
            )
        if confirm_close:
            save_all(root)
        root.quit()
    else:
        root.quit()


def has_unsaved_changes(tab):
    content = tab.textbox.get("1.0", "end-1c")
    return content != tab.saved_content


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


def toggle_status_bar(editor):
    """Toggle the status bar"""
    if editor.status_bar:
        # Toggle status bar visibility
        if editor.status_bar.winfo_ismapped():
            editor.status_bar.pack_forget()
        else:
            editor.status_bar.pack(side='bottom', fill='x')
    else:
        # Create status bar if it doesn't exist
        editor.status_bar = create_status_bar(editor)
        editor.status_bar.pack(side='bottom', fill='x')
        # Apply status bar setting to all tabs
    for tab_id in editor.tabs():
        tab = editor.nametowidget(tab_id)
        if editor.status_bar.winfo_ismapped():
            tab.status_bar.pack(side='bottom', fill='x')
        else:
            tab.status_bar.pack_forget()


def create_status_bar(editor):
    """Create Status bar"""
    status_bar = ttk.Label(
        editor,
        text="Line: 1, Column: 1 | Total Characters: 0 | "
        "Encoding: utf-8"
    )
    return status_bar


def update_status_bar(editor, status_bar):
    cursor_pos = editor.current_tab().textbox.index(tk.INSERT)
    line, column = map(int, cursor_pos.split('.'))
    total_char = len(editor.current_tab().textbox.get('1.0', tk.END))
    status_text = f"Line: {line}, Column: {column} | Total Characters: {total_char} | Encoding: utf-8"
    status_bar.config(text=status_text)


def toggle_word_wrap(editor):
    """Toggle word wrap"""
    current_value = editor.current_tab().textbox.cget('wrap')
    new_value = 'none' if current_value == 'word' else 'word'
    editor.current_tab().textbox.configure(wrap=new_value)

    # Apply word wrap setting to all tabs
    for tab_id in editor.tabs():
        tab = editor.nametowidget(tab_id)
        tab.textbox.configure(wrap=new_value)
