# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -Wextra -fPIC

# Source files
SRC = search.c

# Shared library name
LIB_NAME = libsearch.so

# Python wrapper script
PY_WRAPPER = C:\Users\LENOVO\Desktop\PyC-Text-Editor-1\Graphical User Interface\menu_file.py

all: $(LIB_NAME) $(PY_WRAPPER)

$(LIB_NAME): $(SRC)
	$(CC) $(CFLAGS) -shared -o $(LIB_NAME) $(SRC)

$(PY_WRAPPER): $(LIB_NAME)
	echo "import ctypes" > $(PY_WRAPPER)
	echo "lib = ctypes.CDLL('./$(LIB_NAME)')" >> $(PY_WRAPPER)
	echo "def find(search_text):" >> $(PY_WRAPPER)
	echo "    lib.find(ctypes.c_char_p(search_text.encode()))" >> $(PY_WRAPPER)
