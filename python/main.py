import curses
from re import sub
from curses import wrapper
from os import path, system
from sys import argv

WHITE_ON_LIGHT_PURPLE = None
WHITE_ON_BLACK = None
CYAN_ON_BLACK = None

def extract_kw(word):
    return sub(r"[^a-zA-Z]", "", word)

def load_file(stdscr, file_contents):
    global WHITE_ON_BLACK, CYAN_ON_BLACK

    py_keywords = ["False", "None", "True", "and", "assert", "async", "await", "break",
                   "class", "continue", "def", "del", "elif", "else", "except", "finally",
                   "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
                   "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"]

    words = file_contents.split(" ")
    for word in words:
        if (filtered := extract_kw(word)) in py_keywords:
            before, after = word.split(filtered)
            stdscr.addstr(before, WHITE_ON_BLACK)
            stdscr.addstr(filtered, CYAN_ON_BLACK)
            stdscr.addstr(after + " ", WHITE_ON_BLACK)
        else:
            word += " "
            stdscr.addstr(word, WHITE_ON_BLACK)

def reset_colors():
    system("tput init")

def main(stdscr):
    full_path = path.abspath(argv[1])
    if not path.exists(full_path):
        raise Exception("File does not exist")

    stdscr.clear()

    if curses.can_change_color():
        OFF_WHITE_ID = 1
        LIGHT_PURPLE_ID = 2
        curses.init_color(LIGHT_PURPLE_ID, 445, 414, 645)
        curses.init_color(OFF_WHITE_ID, 980, 980, 880)
    else:
        OFF_WHITE_ID = curses.COLOR_WHITE
        LIGHT_PURPLE_ID = curses.COLOR_MAGENTA

    global WHITE_ON_LIGHT_PURPLE, WHITE_ON_BLACK, CYAN_ON_BLACK

    curses.init_pair(1, OFF_WHITE_ID, LIGHT_PURPLE_ID)
    WHITE_ON_LIGHT_PURPLE = curses.color_pair(1)
    curses.init_pair(2, OFF_WHITE_ID, curses.COLOR_BLACK)
    WHITE_ON_BLACK = curses.color_pair(2)

    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    CYAN_ON_BLACK = curses.color_pair(3)

    bold_underline = curses.A_BOLD | curses.A_UNDERLINE

    max_x = int(stdscr.getmaxyx()[1])
    stdscr.addstr(0, 0, f"    MINI EDITOR - POWERED BY PYTHON | Editing File: ~{full_path}{" " * int(max_x - (54 + len(full_path)))}\n\n", bold_underline | WHITE_ON_LIGHT_PURPLE)

    stdscr.refresh()

    with open(full_path, "r") as f:
        file_contents = f.read()

    load_file(stdscr, file_contents)

    stdscr.getkey()
    reset_colors()

wrapper(main)