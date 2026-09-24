import os
import time

from config import (
    APP_NAME,
    MODEL_NAME,
    VERSION,
    MENU_ITEMS,
    HEADER_TOP,
    HEADER_MIDDLE,
    HEADER_BOTTOM
)


# =========================
# SCREEN
# =========================

def clear():
    os.system("clear")


def wait(seconds=0.3):
    time.sleep(seconds)


# =========================
# HEADER
# =========================

def header():
    print(HEADER_TOP)
    print(HEADER_MIDDLE)
    print(f"┃      {MODEL_NAME:<12}┃")
    print(HEADER_BOTTOM)


def title(text):
    print()
    print(f"╭━━━━━━━━ {text} ━━━━━━━━╮")
    print("╰━━━━━━━━━━━━━━━━━━━━━━━━╯")


# =========================
# MAIN MENU
# =========================

def main_menu():
    clear()
    header()

    print()

    for number, name in MENU_ITEMS.items():
        print(f"{number:>2}) {name}")

    print()

    return input("NanoGen > ").strip()


# =========================
# MESSAGES
# =========================

def message(text):
    print(f"\n{APP_NAME} > {text}")


def success(text):
    print(f"\n[+] {text}")


def error(text):
    print(f"\n[!] {text}")


def info(text):
    print(f"\n[*] {text}")


# =========================
# UI ELEMENTS
# =========================

def separator():
    print("────────────────────────────────")


def pause(text="Press Enter to continue..."):
    input(f"\n{text}")


def screen(title_text):
    clear()
    header()
    title(title_text)


# =========================
# LOADING
# =========================

def loading(text="Loading", duration=0.8):
    print()

    steps = 8
    delay = duration / steps

    for i in range(steps):
        dots = "." * ((i % 3) + 1)

        print(
            f"\r{text}{dots}   ",
            end="",
            flush=True
        )

        time.sleep(delay)

    print("\r" + " " * 40 + "\r", end="")


# =========================
# CHAT UI
# =========================

def chat_header(mode):
    clear()
    header()

    title(f"{mode.upper()} CHAT")

    print("Type /exit to return.")
    separator()
    print()


def user_message(text):
    print(f"You  > {text}")


def bot_message(text):
    print(f"Bot  > {text}")


# =========================
# EXIT
# =========================

def goodbye():
    clear()

    print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
    print("┃      NANO GEN        ┃")
    print(f"┃      {MODEL_NAME:<12}┃")
    print("╰━━━━━━━━━━━━━━━━━━━━━━╯")

    print()
    print(f"{APP_NAME} stopped.")
    print(f"Version: {VERSION}")

    wait(0.5)


# =========================
# ERROR SCREEN
# =========================

def error_screen(text):
    clear()
    header()

    title("ERROR")

    print()
    print(text)

    pause()


# =========================
# INFO SCREEN
# =========================

def info_screen(title_text, lines):
    clear()
    header()
    title(title_text)

    print()

    for line in lines:
        print(line)

    pause()


# =========================
# TEST
# =========================

if __name__ == "__main__":

    while True:

        choice = main_menu()

        if choice == "12":
            goodbye()
            break

        elif choice == "":
            error("Please select an option.")
            wait()

        else:
            print()
            info(f"Selected option: {choice}")
            pause()
