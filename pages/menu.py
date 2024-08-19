import curses
from layout import display_layout
from pages.tools.system_time import display_system_time_menu
from pages.tools.power_scheme import display_power_management_menu
from pages.tools.network import display_network_menu
from pages.tools.system_page import display_system_info_menu
from utils.curses_utils import draw_page_location, get_screen_size, draw_page_keys


def display_main_menu(stdscr):
    """
    Displays the main menu with options to navigate to
    ... different functionalities.
    """
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(500)

    selected_tool_index = 0
    menu_options = [
        ("Power Management", display_power_management_menu),
        ("System Time", display_system_time_menu),
        ("Network Configuration", display_network_menu),
        ("System Information", display_system_info_menu)
    ]
    
    while True:
        stdscr.clear()

        # layout
        layout = display_layout(stdscr)
        header_y_pos = layout['header']
        footer_y_pos = layout['footer']

        # screen
        screen = get_screen_size(stdscr)
        screen_y = screen['y']
        screen_x = screen['x']

        draw_page_location(stdscr, header_y_pos, "Main Menu")
        draw_page_keys(stdscr, footer_y_pos, [
            "'enter': Select",
            "'q': Quit",
            "Use arrow keys to navigate."
        ])

        # calculate menu positioning
        menu_height = len(menu_options) + 2
        menu_width = max(len(menu_name) for menu_name, menu_function in menu_options) + 2

        menu_x_start = (screen_x - menu_width) // 2
        menu_y_start = (screen_y - menu_height) // 2
        tools_y_start = menu_y_start + 1
       
        for menu_no, (menu_name, menu_function) in enumerate(menu_options):
            menu_marker = ">>" if menu_no == selected_tool_index else "  "
            menu_text = f"{menu_marker} {menu_name}"
            stdscr.addstr(tools_y_start + menu_no, menu_x_start, menu_text)

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            selected_tool_index = (selected_tool_index - 1) % len(menu_options)
        elif key == curses.KEY_DOWN:
            selected_tool_index = (selected_tool_index + 1) % len(menu_options)
        elif key == ord('\n'):
            menu_name, menu_function = menu_options[selected_tool_index]
            stdscr.clear()
            menu_function(stdscr)

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(display_main_menu)
