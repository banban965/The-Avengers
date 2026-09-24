import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


APP_NAME = "Nano Gen"
MODEL = "GEN-7M"


def clear():
    os.system("clear")


def run(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip()

        if not output:
            output = result.stderr.strip()

        return output or "No output."

    except Exception as e:
        return f"Error: {e}"


def python_info():
    print("Python")
    print("──────")
    print("Version :", platform.python_version())
    print("Path    :", sys.executable)


def system_info():
    print("\nSystem")
    print("──────")
    print("OS      :", platform.system())
    print("Release :", platform.release())
    print("Machine :", platform.machine())
    print("Arch    :", platform.architecture()[0])


def storage_info():
    print("\nStorage")
    print("───────")

    try:
        total, used, free = shutil.disk_usage(Path.home())

        print(f"Total : {total / (1024**3):.2f} GB")
        print(f"Used  : {used / (1024**3):.2f} GB")
        print(f"Free  : {free / (1024**3):.2f} GB")

    except Exception as e:
        print("Storage error:", e)


def termux_info():
    clear()

    print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
    print("┃      NANO GEN        ┃")
    print("┃     TERMUX MODE      ┃")
    print("╰━━━━━━━━━━━━━━━━━━━━━━╯")

    print()

    python_info()
    system_info()
    storage_info()

    print("\nTermux")
    print("──────")

    print("HOME :", os.environ.get("HOME", "Unknown"))
    print("PREFIX:", os.environ.get("PREFIX", "Unknown"))

    print("\nPackages")

    print("Python :", run(["python", "--version"]))
    print("Termux :", run(["termux-info"]))

    input("\nPress Enter to return...")


def show_environment():
    clear()

    print("╭──── ENVIRONMENT ────╮")

    variables = [
        "HOME",
        "PREFIX",
        "TMPDIR",
        "PATH",
        "SHELL"
    ]

    for name in variables:
        value = os.environ.get(name, "Not set")

        if name == "PATH":
            value = value.split(":")[0] + ":..."

        print(f"│ {name:<8}: {value}")

    print("╰──────────────────────╯")

    input("\nPress Enter...")


def termux_menu():
    while True:
        clear()

        print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
        print("┃      NANO GEN        ┃")
        print("┃     TERMUX MODE      ┃")
        print("╰━━━━━━━━━━━━━━━━━━━━━━╯")

        print()
        print("1) Termux Info")
        print("2) Environment")
        print("3) Python Info")
        print("4) Storage Info")
        print("0) Back")

        choice = input("\nTermux > ").strip()

        if choice == "1":
            termux_info()

        elif choice == "2":
            show_environment()

        elif choice == "3":
            clear()
            python_info()
            input("\nPress Enter...")

        elif choice == "4":
            clear()
            storage_info()
            input("\nPress Enter...")

        elif choice == "0":
            break

        else:
            print("Invalid option.")
            input("Press Enter...")


if __name__ == "__main__":
    termux_menu()
