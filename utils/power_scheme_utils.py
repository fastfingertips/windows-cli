import subprocess

def get_power_schemes():
    """
    retrieves the power schemes and the active power scheme.
    """
    commands = {
        'list': ['powercfg', '/list'],
        'query': ['powercfg', '/query', 'SCHEME_CURRENT', 'SUB_SLEEP', 'STANDBYIDLE'],
    }

    # get the active power scheme
    result = subprocess.run(commands['list'], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    active_scheme = None
    power_schemes = []

    for line in lines:
        if all(x in line for x in ['*', ':']):
            line = line.split(': ')[1].split('(')
            guid = line[0].strip()
            name = line[1].split(')')[0]

            active_scheme = {
                'name': name,
                'guid': guid,
            }
        elif 'Power Scheme GUID' in line:
            line = line.split(': ')[1].split('(')
            guid = line[0].strip()
            name = line[1].split(')')[0]

            power_schemes.append({
                'name': name,
                'guid': guid,
            })

    return active_scheme, power_schemes

def switch_power_scheme(guid: str) -> None:
    """
    activates the power scheme with the given guid.
    """
    subprocess.run(['powercfg', '/setactive', guid])

if __name__ == "__main__":
    active_scheme, power_schemes = get_power_schemes()
    
    print("Active Power Scheme:")
    if active_scheme:
        print(f"Name: {active_scheme['name']}, GUID: {active_scheme['guid']}")
    else:
        print("No active power scheme found.")
    
    print("\nAvailable Power Schemes:")
    for scheme in power_schemes:
        print(f"Name: {scheme['name']}, GUID: {scheme['guid']}")
