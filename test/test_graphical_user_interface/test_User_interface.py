#!/usr/bin/env python3
"""Module to test user interface"""

import os
import pytest
from graphical_user_interface.User_Interface import TextEditorBase, Tab, run
import tempfile


@pytest.fixture
def text_editor():
    return TextEditorBase()


def test_initial_tab_creation(text_editor):
    assert text_editor.index("end") == 2  # There should be two tabs initially


def test_add_tab(text_editor):
    initial_tab_count = text_editor.index("end")
    text_editor.add_tab()
    assert text_editor.index("end") == initial_tab_count + 2


def test_move_tab(text_editor):
    # Add a few tabs
    for _ in range(5):
        text_editor.add_tab()
    initial_tb_postn = [text_editor.indexed_tab(i).winfo_y() for i in range(5)]

    # Simulate moving the tabs
    event_mock = type('EventMock', (object,), {'x': 0, 'widget': text_editor})
    text_editor.move_tab(event_mock)

    # Check if the tabs have moved
    for i in range(5):
        assert text_editor.indexed_tab(i).winfo_y() == initial_tb_postn[i] - 0


def test_right_click_menu_creation(text_editor):
    # Access the right-click menu attribute
    right_click_menu = text_editor.right_click_menu
    # Check if the right-click menu is not None
    assert right_click_menu is not None


def test_copy_cut_paste_text(text_editor):
    # Insert some text
    text_editor.current_tab().textbox.insert('end', 'Hello, World!')
    # Copy the text
    text_editor.copy_text()
    assert text_editor.clipboard_get() is not None
    # Cut the text
    text_editor.cut_text()
    assert text_editor.current_tab().textbox.get('1.0', 'end') is not None
    assert text_editor.clipboard_get() is not None
    # Paste the text
    text_editor.paste_text()
    assert text_editor.current_tab().textbox.get('1.0', 'end') is not None


def test_run_without_errors():
    try:
        run()
    except Exception as e:
        pytest.fail(f"Running the application raised an exception: {e}")


@pytest.fixture
def tab_with_file():
    # Create a temporary test file
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("Test content")

    # Get the path of the temporary file
    temp_file_path = temp_file.name

    # Create a Tab instance with the test file
    tab = Tab(FileDir=temp_file_path)

    yield tab

    # Clean up: Remove the temporary test file
    os.remove(temp_file_path)


def test_load_file_content(tab_with_file):
    # Check if the content of the file is loaded into the text widget
    assert tab_with_file.textbox.get("1.0", "end-1c") == "Test content"


def test_get_file_path(tab_with_file):
    # Check if the file path returned matches the path used to create the tab
    assert tab_with_file.get_file_path() is not None


def test_explain_with_chatgpt(tab_with_file, monkeypatch):
    # Mock subprocess.Popen to avoid actual execution of the Node.js script
    class MockProcess:
        def communicate(self):
            return (b"ChatGPT response", None)
    monkeypatch.setattr(
        "subprocess.Popen", lambda *args, **kwargs: MockProcess()
        )

    # Call explain_with_chatgpt method with None as editor
    with pytest.raises(AttributeError) as e:
        tab_with_file.explain_with_chatgpt(None)

    # Check that the AttributeError is raised with the expected message
    assert str(e.value) == "'NoneType' object has no attribute 'current_tab'"
