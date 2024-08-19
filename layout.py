import curses
from utils.network_utils import get_network_adapters_status
from utils.system_time_utils import get_current_datetime
from utils.curses_utils import draw_text, display_horizontal_line
from utils.system_utils import get_username

def display_layout(stdscr):
    """
    Combines the layout elements like current time, username, header, and footer.
    """
    stdscr.clear()
    sc_height, sc_width = stdscr.getmaxyx()

    # display username
    username = get_username()
    draw_text(stdscr, 0, 0, username)

    display_network_status_icons(stdscr)

    # display header and get its position
    header_y_pos = display_header(stdscr)

    current_datetime = get_current_datetime()
    stdscr.addstr(sc_height - 1, sc_width - len(current_datetime) - 1, current_datetime, curses.A_DIM)

    footer_y_pos = display_footer(stdscr)

    stdscr.refresh()

    return {
        'header': header_y_pos,
        'footer': footer_y_pos
    }

def display_header(stdscr, text=""):
    """
    Displays a header text in the center at the specified y position.
    Returns the position (x_pos, y_pos) of the header.
    """
    sc_height, sc_width = stdscr.getmaxyx()

    text_y_pos = 0
    line_y_pos = 1

    text_x_start = (sc_width - len(text)) // 2
    text_x_end = text_x_start + len(text)

    if text:
        draw_text(
            stdscr,
            text_x_start,
            text_y_pos,
            text,
            curses.A_BOLD | curses.A_UNDERLINE
        )

    display_horizontal_line(stdscr, line_y_pos, sc_width)

    return line_y_pos

def display_footer(stdscr, text=""):
    """
    Displays a footer text in the center at the bottom of the screen.
    If y_pos is None, it will display at the bottom-most row.
    Returns the position (x_pos, y_pos) of the footer.
    """
    sc_height, sc_width = stdscr.getmaxyx()

    # text: screen width is divided by 2 and the text is placed in the center
    text_x_start = (sc_width - len(text)) // 2
    text_x_end = text_x_start + len(text)
    text_y_pos = sc_height - 1

    if text:
        draw_text(
            stdscr,
            text_x_start,
            text_y_pos,
            text,
            curses.A_BOLD | curses.A_UNDERLINE
        )

    # line
    line_y_pos = text_y_pos - 1 # text's one line above
    display_horizontal_line(stdscr, line_y_pos, sc_width)

    return text_y_pos

def display_network_status_icons(stdscr):
    network_adapters = get_network_adapters_status()
    icons = {'Wi-Fi': 'W', 'Ethernet': 'E'}
    status_mapping = {
        'Enabled': '●',
        'Disabled': '○'
    }

    height, width = stdscr.getmaxyx()
    x_offset = width
    y_offset = 0

    icon_width = 4
    spacing = 1
    x_offset -= (len(network_adapters) * (icon_width + spacing) - spacing)

    for adapter in network_adapters:
        interface_name = adapter['interface_name']
        status = adapter['admin_state']
        icon = icons.get(interface_name, '?')
        status_icon = status_mapping.get(status, ' ')

        stdscr.addstr(y_offset, x_offset, f"{icon}: {status_icon} ", curses.A_BOLD)
        x_offset += icon_width + spacing