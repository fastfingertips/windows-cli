import socket
import requests
import subprocess
import os


def get_network_adapters_status():
    """
    Retrieves the current network adapters' status, including their admin
    ... state, connection state, type, and interface name.

    The function runs the 'netsh interface show interface' command and parses
    ... the output into a list  of dictionaries whereeach dictionary contains
    ... details of a network adapter.

    Example output from the command:
    Admin State    State          Type             Interface Name
    -------------------------------------------------------------------------
    Enabled        Connected      Dedicated        Wi-Fi
    Enabled        Connected      Dedicated        Ethernet

    The parsed output returned by the function:
    [
        {
            'admin_state': 'Enabled',
            'state': 'Connected',
            'type': 'Dedicated',
            'interface_name': 'Wi-Fi'
        },
        {
            'admin_state': 'Enabled',
            'state': 'Connected',
            'type': 'Dedicated',
            'interface_name': 'Ethernet'
        }
    ]
    """
    try:
        command_args = ['netsh', 'interface', 'show', 'interface']
        result = subprocess.run(command_args, capture_output=True, text=True, encoding='utf-8')
        output = result.stdout
        lines = output.split('\n')

        adapters = []

        # header to key
        header = lines[1]
        for index, char in enumerate(header):
            if char == ' ' and header[index+1] != ' ' and header[index-1] != ' ':
               header = header[:index] + '_' + header[index + 1:]
        keys = header.lower().split()

        for line in lines:
            if 'Enabled' in line or 'Disabled' in line:
                parts = line.split()
                if len(parts) == 4:
                    adapter = dict(zip(keys, parts))
                    adapters.append(adapter)
        return adapters
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_network_status(host='8.8.8.8', attempts=1):
    """
    Checks network connectivity to a specified host.
    
    :param host: Host to ping (default: '8.8.8.8')
    :param attempts: Number of ping attempts (default: 1)
    :return: String indicating network status
    """
    try:
        # Dynamically ping the host with specified attempts
        result = subprocess.run(
            ['ping', host, '-n', str(attempts)],
            capture_output=True, text=True, encoding='utf-8'
        )
        # Check if any reply was received
        return "Network is up." if "Reply from" in result.stdout else "Network is down."
    except Exception as e:
        return f"Error: {e}"

def get_local_ip():
    """
    Retrieves the local IP address of the machine.
    """
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error as e:
        return f"An error occurred: {e}"

def get_public_ip():
    """
    Retrieves the public IP address of the machine.
    """
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        data = response.json()
        return data['ip']
    except requests.RequestException as e:
        return f"An error occurred: {e}"

def disable_internet(adapter_name):
    """
    Disables internet connection on Windows.
    """
    try:
        os.system(f'netsh interface set interface "{adapter_name}" admin=disable')
        print(f"{adapter_name} has been disabled.")
    except Exception as e:
        print(f"An error occurred: {e}")

def enable_internet(adapter_name):
    """
    Enables internet connection on Windows.
    """
    try:
        os.system(f'netsh interface set interface "{adapter_name}" admin=enable')
        print(f"{adapter_name} has been enabled.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print(get_local_ip())
    print(get_public_ip())
    print(get_network_adapters_status())
    print(get_network_status())