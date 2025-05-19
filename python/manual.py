from sys import argv

def main():
    arg = argv[1] if len(argv) > 1 else None
    if arg is None or arg == "":
        intro()
        commands_man()
    else:
        match arg:
            case "commands":
                commands_man()

            case "keybinds":
                keybinds_man()

            case _:
                print(f"""
\033[1;31mCategory \"{arg}\" is not in the manual.

    Available articles:
        - Commands
        - Keybinds\033[0m
                    """)
                exit(1)

    exit(0)


def intro():
    intro_paragraph = """
[ MINI MANUAL ]
    Mini is a small (hence the name) terminal-based text editor that was written in Python by Zevi Berlin.
    The main purpose is to substitute for GNU-Nano and Vim because Nano sucks and Vim is scary.
    There is a ton of Vim-like functionality built-in while also keeping things easy like Nano.
    
    Current syntax-highlighting is based on file extension, supported languages are:
        - Python (.py)
        - JavaScript (.js | .jsx)
        - HTML/CSS (.html | .htm, .css)
        - Java (.java)
        - C/C++ (.c | .cpp | .h | .hpp)
        - Shell Scripts (.sh, .bash, .zsh)
        
    Enjoy!
    """
    print(intro_paragraph)

def commands_man():
    command_help = """[ COMMAND BAR HELP ]
    The command bar is a small text input box that appears on the bottom of the Mini editor when you press ^C.
    It has a lot of external functionality, but where it really shines are the tools that Mini itself provides.
    
    Mini built-in commands:
        - ':f "string to find"', find a simple string; highlight all instances of said string.
        - ':fr "string to find" | "the string to replace it with"', find a simple string and replace it with another string.
        - ':frp "regex pattern to find" | "the string to replace it with"', find all strings matching a RegEx pattern and replace them.
    
    External commands:
        '! "terminal command"', run a terminal command (does not return output).
    """
    print(command_help)

def keybinds_man():
    keybinds_help = """[ KEYBINDS HELP ]
    There are a ton of keybinds that Mini provides for extra functionality.
    The most commonl and most useful ones are put at the bottom of the Mini editor page by default.
    
    Here is every keybind:
        - '^F': Fast mode, your cursor will move 5 steps at a time instead of 1.
    """
    print(keybinds_help)

if __name__ == "__main__":
    main()