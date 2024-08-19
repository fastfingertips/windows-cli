import curses
from layout import display_layout
from utils.curses_utils import (
  draw_page_location,
  draw_page_keys,
  show_info,
  draw_text
) 
from utils.network_utils import (
  get_network_adapters_status,
  get_network_status,
  disable_internet,
  enable_internet,
  get_public_ip,
  get_local_ip
)


def display_network_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.timeout(-1)

    selected_adapter_index = 0

    while True:
        stdscr.clear()
        adapters = get_network_adapters_status()
        network_status = get_network_status()
        local_ip = get_local_ip()
        public_ip = get_public_ip()

        layout = display_layout(stdscr)
        sc_height, sc_width = stdscr.getmaxyx()

        center_y = sc_height // 2
        center_x = sc_width // 2

        header_y_pos = layout['header']
        footer_y_pos = layout['footer']

        draw_page_location(stdscr, header_y_pos, "Network Configuration")
        draw_page_keys(stdscr, footer_y_pos, [
            "'e': Enable selected adapter",
            "'d': Disable selected adapter",
            "'q': Quit",
            "'h': Go back to main menu",
            "Use arrow keys to navigate."
        ])

        # actions
        for adapter_no, adapter in enumerate(adapters):
            adapter_text = f"> {adapter['interface_name']} ({adapter['admin_state']}, {adapter['state']})"
            adapter_text_y = center_y - adapter_no - 2
            adapter_text_x = center_x - len(adapter_text) // 2
            draw_text(
                stdscr,
                adapter_text_y,
                adapter_text_x,
                adapter_text,
                curses.A_NORMAL if adapter_no != selected_adapter_index else curses.A_REVERSE
            )

        # network status
        lines = [
            f"Network Status: {network_status}",
            f"Local IP Address: {local_ip}",
            f"Public IP Address: {public_ip}"
        ]
        for line_no, line_text in enumerate(lines):
            line_text_y = center_y + line_no
            line_text_x = center_x - len(line_text) // 2
            draw_text(
                stdscr,
                line_text_y,
                line_text_x,
                line_text
            )

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('h'):
            break
        elif key == curses.KEY_UP:
            selected_adapter_index = (selected_adapter_index - 1) % len(adapters)
        elif key == curses.KEY_DOWN:
            selected_adapter_index = (selected_adapter_index + 1) % len(adapters)
        elif key == ord('e'):
            if adapters:
                adapter = adapters[selected_adapter_index]['interface_name']
                enable_internet(adapter)
                show_info(stdscr, f"Enabled {adapter}.")
        elif key == ord('d'):
            if adapters:
                adapter = adapters[selected_adapter_index]['interface_name']
                disable_internet(adapter)
                show_info(stdscr, f"Disabled {adapter}.")

        stdscr.refresh()