import curses
from layout import display_layout
from utils.curses_utils import (
    ScreenSize,
    draw_page_location
)
from utils.power_scheme_utils import(
  get_power_schemes,
  switch_power_scheme
)

def handle_key_press(stdscr, selected_index, power_schemes):
    key = stdscr.getch()
    if key == ord('q'):
        return 0, selected_index
    elif key == curses.KEY_UP:
        selected_index = (selected_index - 1) % len(power_schemes)
    elif key == curses.KEY_DOWN:
        selected_index = (selected_index + 1) % len(power_schemes)
    elif key == ord('\n'):
        switch_power_scheme(guid=power_schemes[selected_index]['guid'])
    return 1, selected_index

def display_power_management_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(-1)

    selected_index = 0
    screen_size = ScreenSize(stdscr)

    while True:
        layout = display_layout(stdscr)
        active_scheme, power_schemes = get_power_schemes()

        header_y_pos = layout['header']        

        draw_page_location(stdscr, header_y_pos, "Power Schemes")
        display_active_scheme(stdscr, active_scheme, screen_size.center_y, screen_size.center_x)
        display_power_schemes(stdscr, power_schemes, selected_index, screen_size.center_y, screen_size.center_x)

        action, selected_index = handle_key_press(stdscr, selected_index, power_schemes)

        if not action:
            break

        screen_size.refresh()

def display_active_scheme(stdscr, active_scheme, center_y, center_x):
    """
    Shows the currently active power scheme at the center of the screen.
    """
    if active_scheme:
        text = f"Active Power Plan: {active_scheme['name']} (GUID: {active_scheme['guid']})"
    else:
        text = "No active power plan found."
    y = center_y - 2
    x = center_x - len(text) // 2
    stdscr.addstr(y, x, text, curses.A_BOLD)

def display_power_schemes(stdscr, power_schemes, selected_index, center_y, center_x):
    """
    Lists available power schemes centered on the screen.
    """
    stdscr.addstr(center_y, center_x - len("Other Power Plans:") // 2, "Other Power Plans:")

    for idx, scheme in enumerate(power_schemes):
        marker = ">>" if idx == selected_index else "  "
        text = f"{marker} {scheme['name']} (GUID: {scheme['guid']})"
        y = center_y + idx + 1
        x = center_x - len(text) // 2
        stdscr.addstr(y, x, text, curses.A_REVERSE if idx == selected_index else curses.A_NORMAL)
