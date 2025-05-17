from curses import wrapper
from sys import argv
from os import path, system

def main(win):
    filepath = path.abspath(argv[1])
    if not path.isfile(filepath):
        raise Exception(f"File not found: {filepath}")

    with open(filepath, "r") as file:
        file_contents = file.read()

    from editor import editor_main
    new_file_contents = editor_main(win, filepath, file_contents)

    with open(filepath, "w") as file:
        file.write(new_file_contents)

    system("tput init")

if __name__ == "__main__":
    wrapper(main)