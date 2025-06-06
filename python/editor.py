import curses
import re
from curses import window
from time import sleep

WHITE_ON_BLACK = None
WHITE_ON_LIGHT_PURPLE = None
max_y = None
max_x = None

def editor_main(stdscr: window, filepath: str, file_content: str):
    file_pad, file_lines, filelength, tool_win = editor_init(stdscr, filepath, file_content)

    file_content = editor_loop(stdscr, filepath, file_content, file_pad, file_lines, filelength, tool_win)

    return file_content

def editor_init(stdscr: window, filepath: str, file_content: str):
    global WHITE_ON_BLACK, WHITE_ON_LIGHT_PURPLE

    curses.curs_set(2)
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

    global max_y, max_x
    max_y, max_x = stdscr.getmaxyx()
    label_win = curses.newwin(1, max_x, 0, 0)
    if (l := len(filepath)) + 50 > max_x:
        if l + 34 > max_x:
            label = str(filepath[:max_x - 1])
        else:
            label = f"    MINI EDITOR | Editing File: ~{filepath}"
    else:
        s = int((max_x - 50 - l) // 2) * " "
        label = f"{s}MINI EDITOR - POWERED BY PYTHON | Editing File: ~{filepath}{s}"

    stdscr.refresh()
    label_win.addstr(label, bold_underline | WHITE_ON_LIGHT_PURPLE)
    label_win.refresh()

    tool_win = curses.newwin(3, max_x, max_y - 4, 0)
    stdscr.refresh()

    help_win = curses.newwin(1, max_x, max_y - 1, 0)
    if max_x > 113:
        s = " " * ((max_x - 114) // 2)
        menu = f"{s}| ^H: Help | ^C: Cmd-Tool | ^X: Exit | ^W: Save | ^F: Fast Mode | ^D: Duplicate | ^K: Cut | ^Z: Undo | ^Y: Redo |{s}"
    else:
        menu = "| ^H: Help |"

    stdscr.refresh()
    help_win.addstr(menu, bold_underline | WHITE_ON_LIGHT_PURPLE)
    help_win.refresh()

    stdscr.move(1, 0)

    file_lines = file_content.split("\n")
    filelength = len(file_lines) + 1

    file_pad = curses.newpad(filelength, max_x)
    stdscr.refresh()
    file_pad.addstr(file_content, WHITE_ON_BLACK)
    file_pad.refresh(0, 0, 1, 0, max_y - 2, max_x)

    stdscr.move(1, 0)

    return file_pad, file_lines, filelength, tool_win

def editor_loop(stdscr: window, filepath: str, file_content: str, file_pad: window, file_lines: list, filelength: int, tool_win: window):
    max_y, max_x = stdscr.getmaxyx()

    fast_mode = False
    command_history = [""]

    while True:
        try:
            key = stdscr.getkey()
            coords = stdscr.getyx()

            match key:
                case "\x18":
                    exit(0)

                case "\x06": # control+f
                    fast_mode = not fast_mode

                case "KEY_UP":
                    if coords[0] == 1:
                        continue  # TODO: Implement the scrolling mechanism for the text pad
                    else:
                        if fast_mode:
                            jmp = 4
                            while coords[0] - jmp < 2:
                                jmp -= 1

                            next_line = file_lines[coords[0] - jmp]
                            if coords[1] >= len(next_line):
                                stdscr.move(coords[0] - jmp - 1, len(next_line))
                            else:
                                stdscr.move(coords[0] - jmp - 1, coords[1])

                        else:
                            next_line = file_lines[coords[0] - 2]
                            if coords[1] >= len(next_line):
                                stdscr.move(coords[0] - 1, len(next_line))
                            else:
                                stdscr.move(coords[0] - 1, coords[1])
                case "KEY_DOWN":
                    if coords[0] + 3 >= max_y:
                        continue
                    elif coords[0] + 1 >= filelength:
                        continue  # TODO: Implement the scrolling mechanism for the text pad

                    else:
                        if fast_mode:
                            jmp = 4
                            while coords[0] + jmp >= filelength - 1:
                                jmp -= 1

                            next_line = file_lines[coords[0] + jmp]
                            if coords[1] >= len(next_line):
                                stdscr.move(coords[0] + jmp + 1, len(next_line))
                            else:
                                stdscr.move(coords[0] + jmp + 1, coords[1])
                        else:
                            next_line = file_lines[coords[0]]
                            if coords[1] >= len(next_line):
                                stdscr.move(coords[0] + 1, len(next_line))
                            else:
                                stdscr.move(coords[0] + 1, coords[1])
                case "KEY_RIGHT":
                    if coords[0] + 1 >= filelength:
                        continue

                    line = file_lines[coords[0] - 1]
                    if coords[1] >= len(line):
                        stdscr.move(coords[0] + 1, 0)
                        continue

                    if fast_mode:
                        jmp = 4
                        while coords[1] + jmp >= len(line) - 1:
                            jmp -= 1
                        stdscr.move(coords[0], coords[1] + jmp)
                    else:
                        stdscr.move(coords[0], coords[1] + 1)
                case "KEY_LEFT":
                    if coords[0] == 1 and coords[1] == 0:
                        continue

                    line = file_lines[coords[0] - 1]
                    if coords[1] == 0:
                        if coords[0] - 2 < 0:
                            continue
                        else:
                            next_line_l = len(file_lines[coords[0] - 2])
                            stdscr.move(coords[0] - 1, next_line_l)
                            continue

                    if fast_mode:
                        jmp = 4
                        while coords[1] - jmp < 0:
                            jmp -= 1
                        stdscr.move(coords[0], coords[1] - jmp)
                    else:
                        stdscr.move(coords[0], coords[1] - 1)


                case "KEY_BACKSPACE": # control+h, idk its weird
                    tool_win.addstr(0, 0, "(^H: Close). The Mini editor is a powerful text editor based on the Python curses library and written by @trynathinkof1 on GitHub", WHITE_ON_LIGHT_PURPLE)
                    tool_win.addstr(1, 0, "Everything you need is in the Mini manual. To access the whole manual, close the editor and run \"mini -man\".", WHITE_ON_LIGHT_PURPLE)
                    tool_win.addstr(2, 0, "    To access a specific manual article such as 'commands' or 'keybinds', close the editor and run \"mini -man <article>\".", WHITE_ON_LIGHT_PURPLE)
                    tool_win.refresh()
                    stdscr.refresh()
                    key = None
                    while key != "KEY_BACKSPACE":
                        try:
                            new_k = stdscr.getkey()
                        except:
                            new_k = None

                        if new_k and new_k == "KEY_BACKSPACE":
                            tool_win.clear()
                            tool_win.refresh()
                            break

                        key = new_k

                    stdscr.move(coords[0], coords[1])
                    continue

                case "\x7f": # backspace
                    print("BACKSPACE")

                case "\x17": # control+w
                    save(filepath, file_content)

                case _:
                    continue

            stdscr.refresh()


        except (KeyboardInterrupt, curses.error):
            key = None
            cmd = ""
            i = -1
            tool_win.addstr(2, 0, "CMD >> ", WHITE_ON_LIGHT_PURPLE)
            while key != "\n":
                try:
                    new_k = stdscr.getkey()
                except:
                    new_k = None

                if new_k and new_k != "\n":
                    if new_k == "\x1b":
                        break
                    elif new_k == "\x7f":
                        cmd = cmd[:-1]
                    elif new_k == "KEY_UP":
                        if abs(i) > len(command_history):
                            cmd = ""
                        else:
                            cmd = command_history[i]
                            i -=1
                    elif new_k == "KEY_DOWN":
                        if abs(i) == 0:
                            cmd = ""
                        else:
                            cmd = command_history[i]
                            i += 1
                    else:
                        cmd += new_k

                key = new_k
                tool_win.clear()
                tool_win.addstr(2, 0, f"CMD >> {cmd}", WHITE_ON_LIGHT_PURPLE)
                tool_win.refresh()

            tool_win.clear()
            tool_win.refresh()
            stdscr.refresh()

            if cmd == ":q" or cmd == "":
                pass

            elif cmd.startswith(":f "):
                string = cmd[3:].strip()[1:-1]
                instance_and_pos = {} # instance number: (y, x)
                instance = iter(range(0, len(file_content)))
                for line in file_lines:
                    if string in line:
                        pos = line.index(string)
                        instance_and_pos[next(instance)] = (file_lines.index(line), pos)

                l = len(instance_and_pos)
                if l == 0:
                    tool_win.addstr(2, 0, f"No instances of \"{string}\" found.", WHITE_ON_LIGHT_PURPLE)
                    tool_win.refresh()
                    sleep(2.5)
                    tool_win.clear()
                    tool_win.refresh()
                    stdscr.refresh()
                else:
                    stdscr.move(instance_and_pos[0][0] + 1, instance_and_pos[0][1])

                    _find_movement_loop(stdscr, instance_and_pos, l)
                    stdscr.refresh()

                command_history.append(f":f \"{string}\"")

            elif cmd.startswith(":fp"):
                pattern = rf"{cmd[3:].strip()[1:-1]}"
                instance_and_pos = {}
                instance = iter(range(0, len(file_content)))
                for line in file_lines:
                    if len(strs := re.findall(pattern, line)) > 0:
                        for s in strs:
                            pos = line.index(s)
                            instance_and_pos[next(instance)] = (file_lines.index(line), pos)

                l = len(instance_and_pos)
                if l == 0:
                    tool_win.addstr(2, 0, f"No strings matched \"{pattern}\".", WHITE_ON_LIGHT_PURPLE)
                    tool_win.refresh()
                    sleep(2.5)
                    tool_win.clear()
                    tool_win.refresh()
                    stdscr.refresh()
                else:
                    stdscr.move(instance_and_pos[0][0] + 1, instance_and_pos[0][1])

                    _find_movement_loop(stdscr, instance_and_pos, l)
                    stdscr.refresh()

                command_history.append(f":fp \"{pattern}\"")

            elif cmd.startswith(":fr"):
                original, replacement = cmd[3:].strip().split("|")
                original = original[1:-2]
                replacement = replacement[2:-1]
                file_content = file_content.replace(original, replacement)
                update_file_content(file_pad, file_content)
                tool_win.addstr(1, 0, f"{len(re.findall(rf'{original}', file_content))} instances", WHITE_ON_LIGHT_PURPLE)
                tool_win.addstr(2, 0, f"of replacing \"{original}\" with \"{replacement}\".", WHITE_ON_LIGHT_PURPLE)
                tool_win.refresh()
                sleep(2.5)
                tool_win.clear()
                stdscr.refresh()

                command_history.append(f":fr \"{original}\" | \"{replacement}\"")

            elif cmd.startswith(":frp"):
                pattern, replacement = cmd[3:].strip().split("|")
                pattern = rf"{pattern[1:-2]}"
                replacement = replacement[2:-1]
                instances = len(re.findall(pattern, file_content))
                file_content = re.sub(pattern, replacement, file_content)
                update_file_content(file_pad, file_content)
                tool_win.addstr(1, 0, f"{instances} instances of replacing", WHITE_ON_LIGHT_PURPLE)
                tool_win.addstr(2, 0, f"strings that match\"{pattern}\" with \"{replacement}\".", WHITE_ON_LIGHT_PURPLE)
                tool_win.refresh()
                sleep(2.5)
                tool_win.clear()
                stdscr.refresh()

                command_history.append(f":frp \"{pattern}\" | \"{replacement}\"")

            else:
                tool_win.addstr(1, 0, f"Command \"{cmd}\" not recognized.", WHITE_ON_LIGHT_PURPLE)
                tool_win.addstr(2, 0, "Close the editor and type \"mini -man commands\" for a list of commands.", WHITE_ON_LIGHT_PURPLE)
                tool_win.refresh()
                sleep(2.5)
                tool_win.clear()
                tool_win.refresh()

            try:
                coords = coords
            except:
                coords = stdscr.getyx()

            stdscr.move(coords[0], coords[1])
            continue

def detect_edit(stdscr, file_pad, file_lines, filelength):
    pass

def update_file_content(file_pad: curses.window, file_content: str):
    file_pad.clear()
    file_pad.addstr(0, 0, file_content, WHITE_ON_BLACK)
    file_pad.refresh(0, 0, 1, 0, max_y - 1, max_x - 1)
    return

def save(filepath: str, file_content: str):
    with open(filepath, "w") as f:
        f.write(file_content)

    return


def _find_movement_loop(stdscr, instance_and_pos, l):
    cur_instance = 0
    key = None
    while key != "\x1b":
        try:
            new_k = stdscr.getkey()
        except:
            new_k = None

        if new_k:
            match new_k:
                case "\x1b":
                    break

                case "KEY_UP":
                    if l == cur_instance or cur_instance == 0:
                        continue
                    else:
                        cur_instance -= 1
                        stdscr.move(instance_and_pos[cur_instance][0] + 1, instance_and_pos[cur_instance][1])

                case "KEY_DOWN":
                    if cur_instance == l - 1:
                        continue
                    else:
                        cur_instance += 1
                        stdscr.move(instance_and_pos[cur_instance][0] + 1, instance_and_pos[cur_instance][1])

        key = new_k
    return