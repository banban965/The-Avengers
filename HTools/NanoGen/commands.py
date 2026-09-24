from pathlib import Path
import json
import os
import time

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def clear():
    os.system("clear")


def command_help():
    print("""
╭━━━━━━━━ COMMAND MODE ━━━━━━━━╮
┃ /help      Command list      ┃
┃ /model     Show model        ┃
┃ /name      Show bot name     ┃
┃ /stats     Show statistics   ┃
┃ /settings  Show settings     ┃
┃ /db        Database info     ┃
┃ /clear     Clear screen      ┃
┃ /time      Current time      ┃
┃ /exit      Return            ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
""")


def show_model():
    print("Model : GEN-7M")


def show_name():
    print("Name  : Nano Gen")


def show_stats():
    stats_file = DATA_DIR / "stats.json"

    if not stats_file.exists():
        print("No statistics found.")
        return

    try:
        with open(stats_file, "r", encoding="utf-8") as f:
            stats = json.load(f)

        print("\n╭──── STATS ────╮")

        for key, value in stats.items():
            print(f"│ {key:<14}: {value}")

        print("╰────────────────╯")

    except Exception as e:
        print(f"Stats error: {e}")


def show_settings():
    settings_file = DATA_DIR / "settings.json"

    if not settings_file.exists():
        print("Settings file not found.")
        return

    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)

        print("\n╭──── SETTINGS ────╮")

        for key, value in settings.items():
            print(f"│ {key:<12}: {value}")

        print("╰───────────────────╯")

    except Exception as e:
        print(f"Settings error: {e}")


def database_info():
    db_file = DATA_DIR / "answers.json"

    if not db_file.exists():
        print("Database not found.")
        return

    try:
        with open(db_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("\n╭──── DATABASE ────╮")
        print(f"│ File    : answers.json")
        print(f"│ Answers : {len(data)}")
        print("╰───────────────────╯")

    except Exception as e:
        print(f"Database error: {e}")


def show_time():
    print("Time:", time.strftime("%Y-%m-%d %H:%M:%S"))


def execute(command):
    command = command.strip().lower()

    if command == "/help":
        command_help()

    elif command == "/model":
        show_model()

    elif command == "/name":
        show_name()

    elif command == "/stats":
        show_stats()

    elif command == "/settings":
        show_settings()

    elif command == "/db":
        database_info()

    elif command == "/clear":
        clear()

    elif command == "/time":
        show_time()

    elif command == "/exit":
        return False

    else:
        print("Unknown command.")
        print("Use /help")

    return True


def command_mode():
    clear()

    print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
    print("┃      NANO GEN        ┃")
    print("┃     COMMAND MODE     ┃")
    print("╰━━━━━━━━━━━━━━━━━━━━━━╯")

    command_help()

    while True:
        try:
            command = input("\nCMD > ")

        except KeyboardInterrupt:
            print()
            break

        if not execute(command):
            break

        time.sleep(0.1)


if __name__ == "__main__":
    command_mode()
