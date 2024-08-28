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
    start_row = 2
    error_message = "Error: System info not available"
    
    fields = [
        ("System", system_info.get('system', 'N/A')),
        ("Node Name", system_info.get('node_name', 'N/A')),
        ("Release", system_info.get('release', 'N/A')),
        ("Version", system_info.get('version', 'N/A')),
        ("Machine", system_info.get('machine', 'N/A')),
        ("Processor", system_info.get('processor', 'N/A')),
        ("Architecture", system_info.get('architecture', 'N/A')),
        ("CPU Usage", f"{system_info.get('cpu_usage', 'N/A')}%"),
        ("Memory Usage", f"{system_info.get('memory_usage', 'N/A')}%")
    ]

    if isinstance(system_info, dict) and system_info:
        for idx, (label, value) in enumerate(fields):
            stdscr.addstr(start_row + idx, 0, f"{label:15}: {value}")
    else:
        stdscr.addstr(start_row, 0, error_message)

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
