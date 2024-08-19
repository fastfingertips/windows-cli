import curses
from utils.curses_utils import show_info
from utils.network_utils import (
  get_network_status,
  get_local_ip,
  get_public_ip,
  get_network_adapters_status,
  enable_internet,
  disable_internet
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

        stdscr.addstr(0, 0, "Network Configuration (q to quit, h for main menu):")
        stdscr.addstr(2, 0, f"Network Status: {network_status}")        
        stdscr.addstr(4, 0, f"Local IP Address: {local_ip}")
        stdscr.addstr(5, 0, f"Public IP Address: {public_ip}")
        stdscr.addstr(7, 0, "Network Adapters:")

        for i, adapter in enumerate(adapters):
            name = adapter['interface_name']
            admin_state = adapter['admin_state']
            status = adapter['state']
            if i == selected_adapter_index:
                stdscr.addstr(8 + i, 0, f"> {name} ({admin_state}, {status})", curses.A_REVERSE)
            else:
                stdscr.addstr(8 + i, 0, f"  {name} ({admin_state}, {status})")

        stdscr.addstr(8 + len(adapters) + 1, 0, "Press 'e' to enable selected adapter.")
        stdscr.addstr(8 + len(adapters) + 2, 0, "Press 'd' to disable selected adapter.")
        stdscr.addstr(8 + len(adapters) + 3, 0, "Use arrow keys to navigate.")

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