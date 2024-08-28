from functools import wraps
from typing import Tuple

import curses
import time

class ScreenSize:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.update_size()

    def update_size(self):
        """Update screen size attributes."""
        self.y, self.x = self.stdscr.getmaxyx()
        self.center_y = self.y // 2
        self.center_x = self.x // 2

    def refresh(self):
        """Refresh the screen size if the terminal is resized."""
        self.update_size()

def get_user_input(stdscr, prompt="Input: ", start_row=2) -> str:
    erase_char = curses.erasechar()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    
    input_buffer = []
    
    while True:
        ch = stdscr.getch()
        
        if ch == curses.KEY_ENTER or ch == 10:
            break
        
        if ch == erase_char[0]:
            if input_buffer:
                input_buffer.pop()
                stdscr.addstr(start_row, 0, prompt + "".join(input_buffer) + " " * (len(input_buffer) + 1))
        else:
            input_buffer.append(chr(ch))
            stdscr.addstr(start_row, 0, prompt + "".join(input_buffer))
        
        stdscr.refresh()
    
    return "".join(input_buffer)

def getsyx() -> Tuple[int, int]:
    """
    Returns the current cursor position.
    """
    return curses.getsyx()

def clear_screen(func):
    """Decorator to clear the screen before calling the function and refresh after it."""
    @wraps(func)
    def wrapper(stdscr, *args, **kwargs):
        stdscr.clear()
        result = func(stdscr, *args, **kwargs)
        stdscr.refresh()
        return result
    return wrapper

def show_info(stdscr, message, title="Info", display_time=2):
    """
    display an informational window for a specified amount of time.

    :param stdscr: the curses window object
    :param message: the message to display
    :param title: the title of the window
    :param display_time: time in seconds to display the window
    """
    height, width = stdscr.getmaxyx()
    padding = 2
    box_width = max(len(message) + 2 * padding, len(title) + 2 * padding)
    box_height = 5
    start_y = height // 2 - box_height // 2
    start_x = width // 2 - box_width // 2

    info_win = curses.newwin(box_height, box_width, start_y, start_x)
    info_win.box()
    info_win.addstr(1, padding, title, curses.A_BOLD)
    info_win.addstr(3, padding, message)
    info_win.refresh()

    time.sleep(display_time)
    info_win.clear()
    stdscr.refresh()

def draw_text(stdscr, /, y, x, text, *args, **kwargs):
    stdscr.addstr(y, x, text, *args, **kwargs)
    return {"start":x, "end":x+len(text), "pos":y}

def draw_page_location(stdscr, header_y_pos, current_page: str):
    stdscr.addstr(header_y_pos + 1, 0, current_page)

def draw_page_keys(stdscr, footer_y_pos, key_infos: list):
    for i, key_info in enumerate(key_infos):
        stdscr.addstr(footer_y_pos - len(key_infos) + i, 0, key_info)

def display_horizontal_line(stdscr, line_pos: int, width):
    stdscr.hline(line_pos, 0, curses.ACS_HLINE, width)

def display_vertical_line(stdscr, line_pos: int, height):
    stdscr.vline(0, line_pos, curses.ACS_VLINE, height)

def get_centered_text_position(text, screen_size: ScreenSize):
    """
    Returns the x position of the text to be centered on the screen.
    """
    text_length = len(text)
    centered_x = screen_size.center_x - (text_length // 2)
    
    return centered_x