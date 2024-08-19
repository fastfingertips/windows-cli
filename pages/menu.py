import curses
from layout import display_layout
from pages.tools.system_time import display_system_time_menu
from pages.tools.power_scheme import display_power_management_menu
from pages.tools.network import display_network_menu
from pages.tools.system_page import display_system_info_menu

def load_menu_options():
    """
    Loads menu options dynamically. This can be extended
    ... to load from a configuration file or database.
    """
    return [
        ("Power Management", display_power_management_menu),
        ("System Time", display_system_time_menu),
        ("Network Configuration", display_network_menu),
        ("System Information", display_system_info_menu)
    ]

def display_main_menu(stdscr):
    """
    Displays the main menu with options to navigate to
    ... different functionalities.
    """
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(500)

    menu_options = load_menu_options()
    selected_idx = 0

    while True:
        stdscr.clear()

        layout = display_layout(stdscr)
        height, width = stdscr.getmaxyx()

        # calculate menu positioning
        num_options = len(menu_options)
        menu_height = num_options + 2
        menu_width = max(len(label) for label, _ in menu_options) + 2

        header_x_pos, header_y_pos = layout['header']
        footer_x_pos, footer_y_pos = layout['footer']

        menu_x_start = (width - menu_width) // 2
        menu_y_start = (height - menu_height) // 2
        tools_y_start = menu_y_start + 1

        # display menu options centered
        stdscr.addstr(menu_y_start, menu_x_start, "Main Menu:")
        for idx, (label, _) in enumerate(menu_options):
            marker = ">>" if idx == selected_idx else "  "
            stdscr.addstr(tools_y_start + idx, menu_x_start, f"{marker} {label}")

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            selected_idx = (selected_idx - 1) % len(menu_options)
        elif key == curses.KEY_DOWN:
            selected_idx = (selected_idx + 1) % len(menu_options)
        elif key == ord('\n'):
            _, function = menu_options[selected_idx]
            stdscr.clear()
            function(stdscr)

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(display_main_menu)
