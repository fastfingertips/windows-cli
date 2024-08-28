import curses
from utils.network_utils import get_network_adapters_status
from utils.system_time_utils import get_current_datetime
from utils.system_utils import get_username
from utils.curses_utils import (
  ScreenSize,
  draw_text,
  display_horizontal_line,
  get_centered_text_position
)


def display_layout(stdscr):
    """
    Combines the layout elements like current time, username, header, and footer.
    """
    stdscr.clear()
    screen_size = ScreenSize(stdscr)
    username = get_username()
    current_datetime = get_current_datetime()

    header_y = display_header(stdscr, screen_size)
    footer_y = display_footer(stdscr, screen_size)

    draw_text(stdscr, header_y - 1, 0, username)
    display_network_status_icons(stdscr, screen_size)
    
    stdscr.addstr(
        footer_y + 1,
        screen_size.x - len(current_datetime) - 1,
        current_datetime,
        curses.A_DIM
    )

    return {
        'header': header_y,
        'footer': footer_y
    }

def display_header(stdscr, screen_size: ScreenSize, line_pos:int = 1, text:str = "") -> int:
    """
    Displays a header text in the center at the specified y position.
    Returns the position (x_pos, y_pos) of the header.
    """
    text_pos = (
        line_pos - 1,
        get_centered_text_position(text, screen_size)
    )

    if text:
        try:
            draw_text(
                stdscr,
                *text_pos,
                text,
                curses.A_BOLD | curses.A_UNDERLINE
            )
        except curses.error:
            curses.endwin()
            print("Error header:", curses.error)

    display_horizontal_line(stdscr, line_pos, screen_size.x)
    return line_pos

def display_footer(stdscr, screen_size: ScreenSize, line_pos:int = None, text:str = "") -> int:
    """
    Displays a footer text in the center at the bottom of the screen.
    If y_pos is None, it will display at the bottom-most row.
    Returns the position (x_pos, y_pos) of the footer.
    """
    if not line_pos:
        line_pos = screen_size.y - 2
    
    text_pos = (
        line_pos + 1,
        get_centered_text_position(text, screen_size)
    )

    if text:
        try:
            draw_text(
                stdscr,
                *text_pos,
                text,
                curses.A_BOLD | curses.A_UNDERLINE
            )
        except curses.error:
            curses.endwin()
            print("Error footer:", curses.error)

    display_horizontal_line(stdscr, line_pos, screen_size.x)
    return line_pos

def display_network_status_icons(stdscr, screen_size: ScreenSize):
    network_adapters = get_network_adapters_status()
    icons = {'Wi-Fi': 'W', 'Ethernet': 'E'}
    status_mapping = {
        'Enabled': '●',
        'Disabled': '○'
    }

    x = screen_size.x
    y = 0

    icon_width = 4
    spacing = 1
    x -= (len(network_adapters) * (icon_width + spacing) - spacing)

    for adapter in network_adapters:
        interface_name = adapter['interface_name']
        status = adapter['admin_state']
        icon = icons.get(interface_name, '?')
        status_icon = status_mapping.get(status, ' ')

        stdscr.addstr(
            y,
            x,
            f"{icon}: {status_icon}",
            curses.A_BOLD
        )
        x += icon_width + spacing