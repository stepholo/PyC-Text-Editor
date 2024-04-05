# PyC Text Editor

PyC Text Editor is a simple yet powerful text editor built using Python and tkinter library. It provides a user-friendly interface for creating, editing, and saving text documents. The main feature of this text editor is the "Explain with ChatGPT" function, which utilizes OpenAI's GPT-3.5 model to provide responses based on the content of the text file.

## Features

- User-friendly interface with tabbed document view.
- Basic text editing functionalities such as copy, cut, paste, undo, and delete.
- File operations including new file creation, opening existing files, saving files, and saving files with different names.
- Ability to save all open tabs at once.
- "Explain with ChatGPT" function that generates responses based on the content of the text file, using OpenAI's GPT-3.5 model.
- Support for customizing font type and size.
- Toggleable status bar to display current cursor position, total characters, and encoding.

## Usage

1. **Creating a New File**: Click on "File" menu and select "New tab" or use the shortcut `Ctrl + N`.

2. **Opening an Existing File**: Click on "File" menu and select "Open" or use the shortcut `Ctrl + O`. Select the file you want to open from the file dialog.

3. **Saving a File**: Click on "File" menu and select "Save" or use the shortcut `Ctrl + S` to save the changes made to the current file. If it's a new file, you will be prompted to specify the file name and location.

4. **Saving All Files**: Click on "File" menu and select "Save All" or use the shortcut `Ctrl + A` to save all open tabs at once.

5. **Explain with ChatGPT**: Click on "Edit" menu and select "Explain with ChatGPT" to generate responses based on the content of the text file using OpenAI's GPT-3.5 model. This will prompt you to re-open the file once the response has been appended to the text file.

6. **Customizing Font**: Click on "Edit" menu, select "Font", and choose the desired font type and size.

7. **Toggle Status Bar**: Click on "View" menu and select "Status Bar" to toggle the visibility of the status bar at the bottom of the window.

8. **Toggle Word Wrap**: Click on "View" menu and select "Word Wrap" to toggle word wrapping for long lines of text.

   ![PyC Text Editor](https://github.com/stepholo/PyC-Text-Editor/blob/main/usage.png)


## Installation

To run the PyC Text Editor, make sure you have Python 3 installed on your system along with the required dependencies listed in `requirements.txt`. You can install the dependencies using the following command:

```
pip install -r requirements.txt
```

After installing the dependencies, navigate to the directory containing `user_interface.py` then run the text editor by executing the `user_interface.py` file:

```
python3 user_interface.py
```

## Dependencies

- Python 3
- tkinter
- Pillow
- OpenAI's GPT-3.5 model (API Key required)
- Node

## Credits

- This project utilizes OpenAI's GPT-3.5 model for the "Explain with ChatGPT" function.
- Icons made by [Freepik](https://www.freepik.com) from [www.flaticon.com](https://www.flaticon.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Stephen Brian Oloo [Twitter](https://twitter.com/Stevenob12) [Linkedin](www.linkedin.com/in/stepholo0)
