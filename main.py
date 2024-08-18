import curses
from pages.menu import display_main_menu

if __name__ == "__main__":
    # start the main menu
    curses.wrapper(display_main_menu)