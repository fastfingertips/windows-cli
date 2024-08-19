import curses
from utils.power_scheme_utils import(
  get_power_schemes,
  switch_power_scheme
)


def display_power_management_menu(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(500)

    selected_idx = 0

    while True:
        height, width = stdscr.getmaxyx()
        center_y = height // 2
        center_x = width // 2

        active_scheme, power_schemes = get_power_schemes()

        stdscr.clear()
        display_active_scheme(stdscr, active_scheme, center_y, center_x)
        display_power_schemes(stdscr, power_schemes, selected_idx, center_y, center_x)

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            selected_idx = (selected_idx - 1) % len(power_schemes)
        elif key == curses.KEY_DOWN:
            selected_idx = (selected_idx + 1) % len(power_schemes)
        elif key == ord('\n'):
            selected_scheme = power_schemes[selected_idx]
            switch_power_scheme(selected_scheme['guid'])
            stdscr.clear()
        elif key == ord('h'):
            break

        stdscr.refresh()

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
        stdscr.addstr(y, x, text)
