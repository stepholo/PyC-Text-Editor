#!/usr/bin/env python3
"""Module to define functions used for Menu options"""

from tkinter import filedialog
import tkinter as tk


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


def close_tab(editor):
    current_index = editor.index(editor.select())
    if current_index != 0:
        editor.forget(current_index)


def exit_editor(root):
    root.quit()