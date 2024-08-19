import curses
from utils.system_time_utils import get_current_datetime


def display_system_time_menu(stdscr):
    """
    Displays the system time menu, showing the current system time.
    """
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.timeout(-1)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "System Time Display:")

        current_datetime = get_current_datetime()
        stdscr.addstr(2, 0, f"Current System Time: {current_datetime}", curses.A_BOLD)

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('h'):
            break

        stdscr.refresh()
