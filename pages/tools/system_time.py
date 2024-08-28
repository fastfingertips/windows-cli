import curses
from utils.curses_utils import ScreenSize, get_centered_text_position
from utils.system_time_utils import get_current_datetime

def handle_key_press(stdscr, key):
    key = stdscr.getch()
    if key == ord('q'):
        return 0

def display_system_time_menu(stdscr):
    """
    Displays the system time menu, showing the current system time.
    """
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.timeout(100)

    screen_size = ScreenSize(stdscr)


    while True:
        current_datetime = get_current_datetime()

        pos = get_centered_text_position(current_datetime, screen_size)
        stdscr.addstr(0, pos, current_datetime)

        key = handle_key_press

        if not key:
            break

        screen_size.refresh()
        stdscr.clear()