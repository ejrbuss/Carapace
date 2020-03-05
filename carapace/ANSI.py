import re

esc = "\033["

# http://ascii-table.com/ansi-escape-sequences.php

def cursor_position(line, column):
    return f'{esc}{line};{column}H'

def cursor_up(n=1):
    return f'{esc}{n}A'

def cursor_down(n=1):
    return f'{esc}{n}B'

def cursor_forward(n=1):
    return f'{esc}{n}C'

def cursor_backward(n=1):
    return f'{esc}{n}D'

cursor_save = f'{esc}s'

cursor_restore = f'{esc}u'

clear_display = f'{esc}2J'

clear_line = f'{esc}K'

reset = f'{esc}0m'

bold = f'{esc}1m'

italics = f'{esc}3m'

underline = f'{esc}4m'

strikethrough = f'{esc}9m'

def foreground(r, g, b):
    return f'{esc}38;2;{r};{g};{b}m'

def background(r, g, b):
    return f'{esc}48;2;{r};{g};{b}m'

def escape(source):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', source)