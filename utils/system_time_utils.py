import subprocess
import time

def get_current_datetime():
    """
    Returns the current date and time as a formatted string.
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")

def capture_current_datetime():
    """
    Retrieves the current system date and time using Windows commands.
    """
    try:
        date_result = subprocess.run(['date', '/T'], capture_output=True, text=True, check=True, shell=True)
        time_result = subprocess.run(['time', '/T'], capture_output=True, text=True, check=True, shell=True)

        current_date = date_result.stdout.strip()
        current_time = time_result.stdout.strip()

        return {
            "date": current_date,
            "time": current_time
        }
    except subprocess.CalledProcessError:
        return "Unable to retrieve date and time."

if __name__ == "__main__":
    print(get_current_datetime())
    print(capture_current_datetime())