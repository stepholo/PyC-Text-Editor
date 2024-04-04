#!/usr/bin/env python3
"""Module to define test cases for Text Editor Menu functions"""

import pytest
from unittest.mock import patch
from tkinter import Tk
import os
from graphical_user_interface.User_Interface import (
    TextEditorBase,
    create_menu,
    create_status_bar
)
import graphical_user_interface.menu_file


@pytest.fixture
def root():
    """Test setup"""
    root = Tk()
    yield root
    root.destroy()


@pytest.fixture
def editor(root):
    """Test Setup"""
    return TextEditorBase(root)


def test_create_menu(root, editor):
    """Test menu creation"""
    create_menu(root, editor)
    # Test if the menu is created successfully
    assert root.nametowidget(".!menu").index("end") > 0


def test_change_font(editor):
    """Test changing font type"""
    # Initial font
    initial_font = editor.current_tab().textbox['font']

    # Change font
    graphical_user_interface.menu_file.change_font(editor, "Arial")

    # Check if font changed successfully
    assert editor.current_tab().textbox['font'] != initial_font
    assert editor.current_tab().textbox['font'][:5] == "Arial"


def test_change_font_size(editor):
    """Test changing font size"""
    # Initial font size
    initial_font_size = editor.current_tab().textbox['font'][1]

    # Change font size
    graphical_user_interface.menu_file.change_font_size(editor, 14)

    # Check if font size changed successfully
    assert editor.current_tab().textbox['font'][1] != initial_font_size
    first = editor.current_tab().textbox['font'][17].strip()
    second = editor.current_tab().textbox['font'][18].strip()
    assert int(first + second) == 14


def test_create_status_bar(editor):
    """Test creation of menu status bar"""
    status_bar = create_status_bar(editor)
    # Test if the status bar is created successfully
    assert status_bar is not None


def test_close_window(root):
    """Test closing the text editor window"""
    # Close the window
    root.withdraw()
    assert root.winfo_exists()


def test_new_file(editor):
    """Test new file creation"""
    initial_tab_count = editor.index("end")
    graphical_user_interface.menu_file.new_file(editor)
    assert editor.index("end") == initial_tab_count + 1


@pytest.fixture
def temp_dir(tmpdir):
    """Create a temporary directory for file operations"""
    return tmpdir.mkdir("temp_files")


def test_open_file(editor):
    """Test open file operation of the text editor"""
    # Create a temporary file with content
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'test1.txt')
    file_content = 'Test content for save_as function'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_content)

    # Open the temporary file
    graphical_user_interface.menu_file.open_file(editor)

    # Check if the content is loaded into the editor
    assert editor.current_tab().textbox.get("1.0", "end-1c") == file_content


def test_save_file(editor, temp_dir):
    """Test save file function of the text editor"""
    # Set up a temporary file
    file_path = temp_dir.join("test.txt")
    tab = editor.current_tab()
    tab.file_dir = str(file_path)
    tab.textbox.insert("1.0", "Test content for save_file function\n")

    # Save the file
    graphical_user_interface.menu_file.save_file(editor)

    # Check if the file is saved correctly
    file_content = file_path.read_text('utf-8').strip()
    text_box_content = tab.textbox.get("1.0", "end-1c").strip()
    assert file_content == text_box_content


def test_save_as(editor):
    """Test Save As operation of the text editor"""
    # Set up a temporary file
    file_content = "Test content for save_as function"
    tab = editor.current_tab()
    tab.textbox.insert("1.0", file_content)

    # Save the file with a new name
    graphical_user_interface.menu_file.save_as(editor)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    expected_file_path = os.path.join(current_dir, 'test_new.txt')
    expected_file_path = os.path.normcase(expected_file_path)
    file_path = os.path.normcase(editor.current_tab().file_dir)
    assert file_path == expected_file_path


def test_save_all(editor, temp_dir):
    """Test Save all function for the text editor"""
    # Set up multiple tabs with different contents
    file_contents = ["Content for save_all function 1\n",
                     "Content for save_all function 2\n",
                     "Content for save_all function 3\n"]
    for i, content in enumerate(file_contents):
        editor.add_tab()
        tab = editor.indexed_tab(i)
        tab.textbox.insert("1.0", content)
        if i > 0:
            tab.file_dir = str(temp_dir.join(f"test_{i}.txt"))

    # Save all files
    graphical_user_interface.menu_file.save_all(editor)

    # Check if all files are saved correctly
    for i, content in enumerate(file_contents):
        if i == 0:
            continue  # Skip the unsaved tab
        file_path = temp_dir.join(f"test_{i}.txt")
        assert file_path.read_text('utf-8').strip() == content.strip()


def test_close_tab(editor):
    """Test closing tabs in the text editor"""
    # Add a new tab
    initial_tab_count = editor.index("end")
    graphical_user_interface.menu_file.new_file(editor)

    # Close the new tab
    graphical_user_interface.menu_file.close_tab(editor)

    # Check if the tab is closed
    assert editor.index("end") == initial_tab_count


def test_exit_editor(editor, temp_dir):
    """Test exit the text editor"""
    # Set up a temporary file with content
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'test.txt')
    file_content = "Test content for exit_editor function"
    tab = editor.current_tab()
    tab.file_dir = str(file_path)
    tab.textbox.insert("1.0", file_content)

    # Mock the user response to the prompt for saving unsaved changes
    with patch('tkinter.messagebox.askyesno', return_value=True):
        # Exit the editor
        graphical_user_interface.menu_file.exit_editor(editor)

    # Check if the file is saved before exiting
    with open(file_path, 'r', encoding='utf-8') as file:
        assert file.read().rstrip('\n') == file_content
