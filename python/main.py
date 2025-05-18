import sys
from curses import wrapper
from os import path, system

def handle_one_line_exception(exc_type, exc_value, exc_traceback):
    print(f"\033[1;31m\n{exc_type.__name__}: {exc_value}\033[0m")
    exit(1)

def main(win):
    filepath = path.abspath(sys.argv[1])
    print(filepath)

    if not path.isfile(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist.\n\tUse 'touch {filepath}' to create a new file.\n")

    with open(filepath, "r") as file:
        file_contents = file.read()

    from editor import editor_main
    editor_main(win, filepath, file_contents)

    system("tput init")

if __name__ == "__main__":
    sys.excepthook = handle_one_line_exception
    wrapper(main)