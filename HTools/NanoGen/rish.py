import subprocess
import shutil


APP_NAME = "Nano Gen"
MODEL = "GEN-7M"


READ_ONLY_COMMANDS = {
    "id": "id",
    "whoami": "whoami",
    "pwd": "pwd",
    "android": "getprop ro.build.version.release",
    "model": "getprop ro.product.model",
    "brand": "getprop ro.product.brand",
    "device": "getprop ro.product.device",
    "kernel": "uname -a"
}


def rish_available():
    return shutil.which("rish") is not None


def run_rish(command):
    if not rish_available():
        return "ERROR: rish not found."

    if command not in READ_ONLY_COMMANDS:
        return "BLOCKED: command is not allowed."

    real_command = READ_ONLY_COMMANDS[command]

    try:
        result = subprocess.run(
            ["rish", "-c", real_command],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip()

        if not output:
            output = result.stderr.strip()

        return output or "No output."

    except subprocess.TimeoutExpired:
        return "ERROR: rish command timed out."

    except Exception as e:
        return f"ERROR: {e}"


def show_command(name):
    print(f"\n[{name}]")
    print("─" * 30)
    print(run_rish(name))


def rish_menu():
    while True:
        print()
        print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
        print("┃      NANO GEN        ┃")
        print("┃      RISH MODE       ┃")
        print("╰━━━━━━━━━━━━━━━━━━━━━━╯")
        print()
        print("1) ID")
        print("2) Android Version")
        print("3) Device Model")
        print("4) Brand")
        print("5) Device")
        print("6) Kernel")
        print("7) Whoami")
        print("8) PWD")
        print("0) Back")

        choice = input("\nRish > ").strip()

        options = {
            "1": "id",
            "2": "android",
            "3": "model",
            "4": "brand",
            "5": "device",
            "6": "kernel",
            "7": "whoami",
            "8": "pwd"
        }

        if choice == "0":
            break

        command = options.get(choice)

        if command is None:
            print("Invalid option.")
            continue

        show_command(command)
        input("\nPress Enter...")


if __name__ == "__main__":
    rish_menu()
