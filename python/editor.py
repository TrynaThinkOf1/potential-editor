import curses
from curses import window

def editor_main(stdscr: window, filepath: str, file_content: str):
    curses.curs_set(1)
    if curses.can_change_color():
        OFF_WHITE_ID = 1
        LIGHT_PURPLE_ID = 2
        curses.init_color(LIGHT_PURPLE_ID, 445, 414, 645)
        curses.init_color(OFF_WHITE_ID, 980, 980, 880)
    else:
        OFF_WHITE_ID = curses.COLOR_WHITE
        LIGHT_PURPLE_ID = curses.COLOR_MAGENTA

    curses.init_pair(1, OFF_WHITE_ID, LIGHT_PURPLE_ID)
    WHITE_ON_LIGHT_PURPLE = curses.color_pair(1)
    curses.init_pair(2, OFF_WHITE_ID, curses.COLOR_BLACK)
    WHITE_ON_BLACK = curses.color_pair(2)

    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    CYAN_ON_BLACK = curses.color_pair(3)

    bold_underline = curses.A_BOLD | curses.A_UNDERLINE


    max_y, max_x = stdscr.getmaxyx()
    label_win = curses.newwin(1, max_x, 0, 0)
    if (l := len(filepath)) + 54 > max_x:
        if l + 34 > max_x:
            label = f"    MINI EDITOR | Editing File: {filepath.split("/")[-3:]}"
        else:
            label = f"    MINI EDITOR | Editing File: ~{filepath}"
    else:
        filepath = filepath + " " * (max_x - 54 - len(filepath))
        label = f"    MINI EDITOR - POWERED BY PYTHON | Editing File: ~{filepath}{" " * int(max_x - (54 + len(filepath)))}"

    stdscr.refresh()
    label_win.addstr(label, bold_underline | WHITE_ON_LIGHT_PURPLE)
    label_win.refresh()

    stdscr.move(1, 0)

    file_lines = file_content.split("\n")
    filelength = len(file_lines) + 1

    file_pad = curses.newpad(filelength, max_x)
    stdscr.refresh()
    file_pad.addstr(file_content, WHITE_ON_BLACK)
    file_pad.refresh(0, 0, 1, 0, max_y, max_x)

    stdscr.move(1, 0)



    while True:
        key = stdscr.getch()
        coords = stdscr.getyx()

        #print(str(key) + " ")
        if key == 259:
            if coords[0] == 1:
                continue #TODO: Implement the scrolling mechanism for the text pad
            else:
                next_line = file_lines[coords[0] - 2]
                if coords[1] >= len(next_line):
                    stdscr.move(coords[0] - 1, len(next_line))
                else:
                    stdscr.move(coords[0] - 1, coords[1])
        elif key == 258:
            if coords[0] + 1 >= filelength:
                continue  # TODO: Implement the scrolling mechanism for the text pad
            else:
                next_line = file_lines[coords[0]]
                if coords[1] >= len(next_line):
                    stdscr.move(coords[0] + 1, len(next_line))
                else:
                    stdscr.move(coords[0] + 1, coords[1])

        elif key == 261:
            line = file_lines[coords[0] - 1]
            if coords[1] >= len(line):
                stdscr.move(coords[0] + 1, 0)
            else:
                stdscr.move(coords[0], coords[1] + 1)
        elif key == 260:
            if coords[1] == 0:
                if coords[0] == 1:
                    continue
                else:
                    stdscr.move(coords[0] - 1, len(file_lines[coords[0] - 2]))
            else:
                stdscr.move(coords[0], coords[1] - 1)

        stdscr.refresh()

    return file_content