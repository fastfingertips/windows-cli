from functools import wraps
import curses
import time


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
        stdscr.addstr(footer_y_pos - len(key_infos) + i - 1, 0, key_info)

def display_horizontal_line(stdscr, y_pos, screen_width):
    stdscr.hline(y_pos, 0, curses.ACS_HLINE, screen_width)

def display_vertical_line(stdscr, x_pos, screen_height):
    stdscr.vline(0, x_pos, curses.ACS_VLINE, screen_height)

def get_screen_size(stdscr):
    y, x = stdscr.getmaxyx()
    context = {
        "screen": (y, x),
        "center": (y // 2, x // 2)
    }
    return context

def get_centered_text_position(stdscr, text, screen=None):
    """
    Returns the x position of the text to be centered on the screen.
    """
    if not screen:
        screen = get_screen_size(stdscr)

    return (screen['screen'][1] - len(text)) // 2