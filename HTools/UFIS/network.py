import socket
import requests

def network_info():
    print("\n=== Network Info ===")

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        print("Hostname:", hostname)
        print("Local IP:", local_ip)

        public_ip = requests.get(
            "https://api.ipify.org",
            timeout=5
        ).text

        print("Public IP:", public_ip)

    except Exception as e:
        print("Error:", e)