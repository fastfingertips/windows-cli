import subprocess

def get_active_scheme():
    """
    Burada powercfg komutu ile güncel enerji planının ismini alıyoruz.
    """

    commands = {
        'list': ['powercfg', '/list'],
        'query': ['powercfg', '/query', 'SCHEME_CURRENT', 'SUB_SLEEP', 'STANDBYIDLE'],
    }

    result = subprocess.run(commands['list'], capture_output=True, text=True)
    lines = result.stdout.split('\n')

    for line in lines:
        if all(x in line for x in ['*', ':']):
            line = line.split(': ')[1].split('(')
            guid = line[0].strip()
            name = line[1].split(')')[0]

            context = {
                'name': name,
                'guid': guid,
            }

            return context
    return None

current_power_plan = get_active_scheme()
print(current_power_plan)
