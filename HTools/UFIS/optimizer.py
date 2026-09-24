import os
import platform


def system_info():
    print("\n=== UFNS System Optimizer ===")

    print("OS:", platform.system())
    print("Version:", platform.version())


def ping_test():
    print("\n=== Ping Test ===")

    host = "8.8.8.8"

    if os.name == "nt":
        cmd = f"ping -n 4 {host}"
    else:
        cmd = f"ping -c 4 {host}"

    os.system(cmd)


def optimizer():
    system_info()
    ping_test()

    print("\nOptimization check completed.")