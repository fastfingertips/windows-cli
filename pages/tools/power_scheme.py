import curses
from layout import display_layout
from utils.curses_utils import get_screen_size, draw_page_location, clear_screen
from utils.power_scheme_utils import(
  get_power_schemes,
  switch_power_scheme,
)


@clear_screen
def display_power_management_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(-1)

    selected_idx = 0

    while True:
        layout = display_layout(stdscr)
        screen = get_screen_size(stdscr)

        header_y_pos = layout['header']
        screen_center_y = screen['center_y']
        screen_center_x = screen['center_x']

        active_scheme, power_schemes = get_power_schemes()

        draw_page_location(stdscr, header_y_pos, "Power Schemes")
        display_active_scheme(stdscr, active_scheme, screen_center_y, screen_center_x)
        display_power_schemes(stdscr, power_schemes, selected_idx, screen_center_y, screen_center_x)

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            selected_idx = (selected_idx - 1) % len(power_schemes)
        elif key == curses.KEY_DOWN:
            selected_idx = (selected_idx + 1) % len(power_schemes)
        elif key == ord('\n'):
            switch_power_scheme(guid=power_schemes[selected_idx]['guid'])
        elif key == ord('h'):
            break

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

def display_power_schemes(stdscr, power_schemes, selected_idx, center_y, center_x):
    """
    Lists available power schemes centered on the screen.
    """
    stdscr.addstr(center_y, center_x - len("Other Power Plans:") // 2, "Other Power Plans:")

    for idx, scheme in enumerate(power_schemes):
        marker = ">>" if idx == selected_idx else "  "
        text = f"{marker} {scheme['name']} (GUID: {scheme['guid']})"
        y = center_y + idx + 1
        x = center_x - len(text) // 2
        stdscr.addstr(y, x, text, curses.A_REVERSE if idx == selected_idx else curses.A_NORMAL)
