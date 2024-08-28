import curses
from layout import display_layout
from utils.curses_utils import (
  ScreenSize,
  get_centered_text_position,
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


def handle_key_press(stdscr, selected_adapter_index, adapters):
        key = stdscr.getch()
        if key == ord('q'):
            return 0, 0
        elif key == curses.KEY_UP:
            selected_adapter_index = (selected_adapter_index - 1) % len(adapters)
        elif key == curses.KEY_DOWN:
            selected_adapter_index = (selected_adapter_index + 1) % len(adapters)
        elif key == ord('e'):
            if adapters:
                adapter = adapters[selected_adapter_index]
                adapter_name = adapter['interface_name']
                if adapter['admin_state'] == "Disabled":
                    show_info(stdscr, f"Enabling {adapter_name}...", "Network", 1)
                    success = enable_internet(adapter_name)
                    if success:
                        show_info(stdscr, f"Enabled {adapter_name} successfully.", "Network", 1)
                    else:
                        show_info(stdscr, f"Failed to enable {adapter_name}. Administrator privileges may be required.", "Error", 2)
                else:
                    show_info(stdscr, f"{adapter_name} is already enabled.", "Network", .5)
        elif key == ord('d'):
            if adapters:
                adapter = adapters[selected_adapter_index]
                adapter_name = adapter['interface_name']
                if adapter['admin_state'] == "Enabled":
                    show_info(stdscr, f"Disabling {adapter_name}...", "Network", 1)
                    success = disable_internet(adapter_name)
                    if success:
                        show_info(stdscr, f"Disabled {adapter_name} successfully.", "Network", 1)
                    else:
                        show_info(stdscr, f"Failed to disable {adapter_name}. Administrator privileges may be required.", "Error", 2)
                else:
                    show_info(stdscr, f"{adapter_name} is already disabled.", "Network", .5)
        else:
            show_info(stdscr, "Invalid key pressed.", "Key Error", 2)
        return 1, selected_adapter_index

def display_network_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.timeout(-1)

    screen_size = ScreenSize(stdscr)
    selected_adapter_index = 0
    

    while True:
        adapters = get_network_adapters_status()
        network_status = get_network_status()
        local_ip = get_local_ip()
        public_ip = get_public_ip()

        layout = display_layout(stdscr)
        header_y_pos = layout['header']
        footer_y_pos = layout['footer']
        
        draw_page_location(stdscr, header_y_pos, "Network Configuration")
        draw_page_keys(stdscr, footer_y_pos, [
            "'e': Enable selected adapter" if adapters[selected_adapter_index]['admin_state'] != "Enabled" else "'d': Disable selected adapter",
            "'q': Quit",
            "Use arrow keys to navigate."
        ])

        # actions
        for adapter_no, adapter in enumerate(adapters):
            adapter_text = f"> {adapter['interface_name']} ({adapter['admin_state']}, {adapter['state']})"
            adapter_text_y = screen_size.center_y - adapter_no - 2
            adapter_text_x = get_centered_text_position(adapter_text, screen_size)
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
            line_text_y = screen_size.center_y + line_no
            line_text_x = get_centered_text_position(line_text, screen_size)
            draw_text(
                stdscr,
                line_text_y,
                line_text_x,
                line_text
            )

        action, selected_adapter_index = handle_key_press(stdscr, selected_adapter_index, adapters)
        if not action:
            break

        screen_size.refresh()