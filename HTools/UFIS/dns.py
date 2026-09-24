import time
import socket

dns_servers = [
    # Cloudflare
    "1.1.1.1",
    "1.0.0.1",

    # Google
    "8.8.8.8",
    "8.8.4.4",

    # Quad9
    "9.9.9.9",
    "149.112.112.112",

    # OpenDNS
    "208.67.222.222",
    "208.67.220.220",

    # AdGuard
    "94.140.14.14",
    "94.140.15.15",

    # CleanBrowsing
    "185.228.168.9",
    "185.228.169.9",
    "185.228.168.10",
    "185.228.169.11",

    # Comodo
    "8.26.56.26",
    "8.20.247.20",

    # Level3
    "4.2.2.1",
    "4.2.2.2",
    "4.2.2.3",
    "4.2.2.4",
    "4.2.2.5",
    "4.2.2.6",

    # Verisign
    "64.6.64.6",
    "64.6.65.6",

    # Neustar
    "156.154.70.1",
    "156.154.71.1",

    # Alternate DNS
    "76.76.19.19",
    "76.76.20.20",

    # ControlD
    "76.76.2.0",
    "76.76.10.0",

    # DNS.WATCH
    "84.200.69.80",
    "84.200.70.40",

    # Yandex DNS
    "77.88.8.8",
    "77.88.8.1",

    # SafeDNS
    "195.46.39.39",
    "195.46.39.40",

    # Hurricane Electric
    "74.82.42.42",

    # IBM Quad
    "9.9.9.10",
    "149.112.112.10",

    # AliDNS
    "223.5.5.5",
    "223.6.6.6",

    # Baidu
    "180.76.76.76",

    # NTT
    "129.250.35.250"
]

def test_dns(dns):
    try:
        start = time.time()

        socket.gethostbyname("google.com")

        end = time.time()

        return round((end - start) * 1000, 2)

    except:
        return None


def dns_optimizer():
    print("\n=== UFNS DNS Benchmark ===")

    results = {}

    for server in dns_servers:
        speed = test_dns(server)

        if speed:
            results[server] = speed
            print(f"{server} -> {speed} ms")
        else:
            print(f"{server} Failed")

    if results:
        best = min(results, key=results.get)

        print("\n===== RESULT =====")
        print("Fastest DNS:", best)
        print("Latency:", results[best], "ms")