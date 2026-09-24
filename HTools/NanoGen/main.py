import os
import time

from config import (
    APP_NAME,
    MODEL_NAME,
    VERSION,
    ensure_directories
)

from ui import (
    main_menu,
    screen,
    pause,
    error,
    success,
    goodbye
)

from chat import (
    normal_chat,
    hard_chat,
    think_chat
)

from rish import rish_menu
from termux import termux_menu
from commands import command_mode
from reader import print_file
from stats import show_stats, set_start_time
from database import add_answer, count_answers
from settings import load_settings, show_settings


# =========================
# INITIALIZE
# =========================

def initialize():
    ensure_directories()
    load_settings()
    set_start_time()


# =========================
# READER
# =========================

def reader_mode():
    screen("FILE READER")

    print("Supported:")
    print("PDF / MD / TXT / HTML")

    path = input("\nFile path > ").strip()

    if not path:
        return

    print()
    print_file(path)

    pause()


# =========================
# ADD ANSWER
# =========================

def add_answer_mode():
    screen("ADD ANSWER / QUZE")

    print("Teach Nano Gen a new Question → Answer pair.")
    print()

    question = input("Question > ").strip()

    if not question:
        error("Question cannot be empty.")
        pause()
        return

    answer = input("Answer   > ").strip()

    if not answer:
        error("Answer cannot be empty.")
        pause()
        return

    ok, message = add_answer(question, answer)

    if ok:
        success(message)
        print(f"\nDatabase answers: {count_answers()}")
    else:
        error(message)

    pause()


# =========================
# SETTINGS
# =========================

def settings_mode():
    screen("ALL SETTINGS")

    show_settings()

    pause()


# =========================
# ROUTER
# =========================

def route(choice):
    if choice == "1":
        normal_chat()

    elif choice == "2":
        hard_chat()

    elif choice == "3":
        think_chat()

    elif choice == "4":
        rish_menu()

    elif choice == "5":
        termux_menu()

    elif choice == "6":
        from debug import show_debug, save_report

        screen("DEBUG MODE")
        show_debug()

        print()
        report = save_report()

        print(f"\nDebug report: {report}")
        pause()

    elif choice == "7":
        command_mode()

    elif choice == "8":
        reader_mode()

    elif choice == "9":
        screen("RISH STATS")
        show_stats()
        pause()

    elif choice == "10":
        add_answer_mode()

    elif choice == "11":
        settings_mode()

    elif choice == "12":
        return False

    else:
        error("Invalid option.")
        time.sleep(0.7)

    return True


# =========================
# MAIN LOOP
# =========================

def main():
    initialize()

    while True:
        choice = main_menu()

        if not route(choice):
            goodbye()
            break


if __name__ == "__main__":
    main()
