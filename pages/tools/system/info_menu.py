import curses
import platform
from utils.system_utils import get_cpu_usage, get_memory_usage
from utils.curses_utils import draw_text

def get_system_info():
    """
    Returns a dictionary with system information.
    """
    return {
        'system': platform.system(),
        'node_name': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'architecture': platform.architecture(),
        'cpu_usage': get_cpu_usage(),
        'memory_usage': get_memory_usage()
    }

def print_system_info(stdscr, system_info):
    """
    Prints system information to the screen.
    """
    if isinstance(system_info, dict):
        stdscr.addstr(2, 0, f"System: {system_info.get('system', 'N/A')}")
        stdscr.addstr(3, 0, f"Node Name: {system_info.get('node_name', 'N/A')}")
        stdscr.addstr(4, 0, f"Release: {system_info.get('release', 'N/A')}")
        stdscr.addstr(5, 0, f"Version: {system_info.get('version', 'N/A')}")
        stdscr.addstr(6, 0, f"Machine: {system_info.get('machine', 'N/A')}")
        stdscr.addstr(7, 0, f"Processor: {system_info.get('processor', 'N/A')}")
        stdscr.addstr(8, 0, f"Architecture: {system_info.get('architecture', 'N/A')}")
        stdscr.addstr(9, 0, f"CPU Usage: {system_info.get('cpu_usage', 'N/A')}%")
        stdscr.addstr(10, 0, f"Memory Usage: {system_info.get('memory_usage', 'N/A')}%")
    else:
        stdscr.addstr(2, 0, "Error: System info not available")

def display_system_info_menu(stdscr):
    """
    Displays the system information menu.
    """
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.timeout(1000)

    while True:
        system_info = get_system_info()

        draw_text(stdscr, 0, 0, "System Information")
        print_system_info(stdscr, system_info)

        key = stdscr.getch()
        if key == ord('q'):
            break    

if __name__ == "__main__":
    curses.wrapper(display_system_info_menu)
