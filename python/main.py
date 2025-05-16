import curses
from curses import wrapper
from os import path, system
from sys import argv

def reset_colors():
    system("tput init")

def main(stdscr):
    full_path = path.abspath(argv[1])
    if not path.exists(full_path):
        raise Exception("File does not exist")

    with open(full_path, "r") as f:
        file_contents = f.read()

    stdscr.clear()

    if curses.can_change_color():
        OFF_WHITE_ID = 1
        LIGHT_PURPLE_ID = 2
        curses.init_color(LIGHT_PURPLE_ID, 445, 414, 645)
        curses.init_color(OFF_WHITE_ID, 980, 980, 880)


    curses.init_pair(1, OFF_WHITE_ID, LIGHT_PURPLE_ID)
    WHITE_ON_LIGHT_PURPLE = curses.color_pair(1)
    curses.init_pair(2, OFF_WHITE_ID, curses.COLOR_BLACK)
    WHITE_ON_BLACK = curses.color_pair(2)

    bold_underline = curses.A_BOLD | curses.A_UNDERLINE

    max_x = int(stdscr.getmaxyx()[1])
    stdscr.addstr(0, 0, f"    MINI EDITOR - POWERED BY PYTHON | Editing File: ~{full_path}{" " * int(max_x - (54 + len(full_path)))}\n\n", bold_underline | WHITE_ON_LIGHT_PURPLE)

    stdscr.refresh()

    stdscr.addstr(file_contents, WHITE_ON_BLACK)
    stdscr.refresh()

    stdscr.getkey()
    reset_colors()

wrapper(main)