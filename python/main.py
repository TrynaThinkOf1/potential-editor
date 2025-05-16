import curses
from curses import wrapper
from os import path
from sys import argv

def main(stdscr):
    full_path = path.abspath(argv[1])
    if not path.exists(full_path):
        raise Exception("File does not exist")

    with open(full_path, "r") as f:
        file_contents = f.read()

    stdscr.clear()

    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    bold_underline = curses.A_BOLD | curses.A_UNDERLINE | curses.A_REVERSE
    max_x = int(stdscr.getmaxyx()[1])
    stdscr.addstr(0, 0, f"    MINI EDITOR - POWERED BY PYTHON | Editing File: ~{full_path}{" " * int(max_x - (54 + len(full_path)))}\n\n", bold_underline | curses.color_pair(1))

    stdscr.refresh()

    stdscr.addstr(file_contents)
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)