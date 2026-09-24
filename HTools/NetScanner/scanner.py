import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor

NETWORK = "192.168.1."

def check(ip):
    addr = NETWORK + str(ip)
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", addr],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if result.returncode == 0:
        try:
            host = socket.gethostbyaddr(addr)[0]
        except Exception:
            host = "Unknown"

        return {
            "ip": addr,
            "mac": "-",
            "hostname": host
        }

    return None


def scan_network():
    devices = []

    with ThreadPoolExecutor(max_workers=64) as pool:
        for d in pool.map(check, range(1, 255)):
            if d:
                devices.append(d)

    return devices