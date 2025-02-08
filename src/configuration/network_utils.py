from .log_decorator import info_log
import socket
import time


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def network_connected(hostname="google.com"):
    # 📡 test if internet is available
    try:
        host = socket.gethostbyname(hostname)
        socket.create_connection((host, 80), 2).close()
        return True
    except Exception:
        time.sleep(1)
    return False


@info_log
def wait_for_internet_connection(action):
    connection_error_shown = False
    while not network_connected():
        # 🚫 draw error message if not already drawn
        if not connection_error_shown:
            connection_error_shown = True
            action()
        time.sleep(10)
