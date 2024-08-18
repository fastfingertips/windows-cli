import psutil
import os

def get_system_info():
    user = psutil.users()[0]
    return f"System: {user.name} ({user.terminal})"

def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent(interval=1)}%"

def get_memory_usage():
    memory = psutil.virtual_memory()
    return f"Memory Usage: {memory.percent}% used out of {memory.total / (1024 ** 3):.2f} GB"

def get_username():
    """
    Returns the current system's username.
    """
    return os.getlogin()