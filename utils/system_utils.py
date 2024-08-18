import os
import psutil

def get_cpu_usage():
    return f"{psutil.cpu_percent(interval=1)}%"

def get_memory_usage():
    memory = psutil.virtual_memory()
    return f"Memory Usage: {memory.percent}% used out of {memory.total / (1024 ** 3):.2f} GB"

def get_username():
    """
    Returns the current system's username.
    """
    return os.getlogin()

if __name__ == "__main__":
    print(f"CPU Usage: {get_cpu_usage()}")
    print(f"Memory Usage: {get_memory_usage()}")
    print(f"Username: {get_username()}")