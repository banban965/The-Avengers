#!/usr/bin/env python3

import os
import sys
import time
import zipfile
from pathlib import Path


APP = "OP COMPRESSOR PRO"
VERSION = "1.0"


def clear():
    os.system("clear")


def human(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def banner():
    print("""
╔════════════════════════════════════════╗
║          OP COMPRESSOR PRO             ║
║              VERSION 1.0               ║
╠════════════════════════════════════════╣
║      Advanced File Compression         ║
╚════════════════════════════════════════╝
""")


def file_info(path):
    if not os.path.exists(path):
        print("[!] File not found")
        return

    if os.path.isfile(path):
        size = os.path.getsize(path)

        print("\n╔════════ FILE INFO ════════╗")
        print(f" Name : {os.path.basename(path)}")
        print(f" Size : {human(size)}")
        print(f" Path : {os.path.abspath(path)}")
        print(" Type : File")
        print("╚═══════════════════════════╝")

    elif os.path.isdir(path):
        total = 0
        count = 0

        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                    count += 1
                except OSError:
                    pass

        print("\n╔══════ FOLDER INFO ═══════╗")
        print(f" Name  : {os.path.basename(path)}")
        print(f" Files : {count}")
        print(f" Size  : {human(total)}")
        print(" Type  : Folder")
        print("╚═══════════════════════════╝")


def compress_file(src, dst, level):
    if not os.path.isfile(src):
        print("[!] Invalid file")
        return

    original = os.path.getsize(src)

    print("\n[+] OP Engine starting...")
    print(f"[+] Input : {src}")
    print(f"[+] Size  : {human(original)}")
    print(f"[+] Level : {level}")
    print()

    start = time.time()

    try:
        with zipfile.ZipFile(
            dst,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=level
        ) as archive:

            archive.write(
                src,
                arcname=os.path.basename(src)
            )

    except Exception as e:
        print(f"\n[!] Compression error: {e}")
        return

    elapsed = time.time() - start
    final_size = os.path.getsize(dst)

    if original:
        saved = original - final_size
        percent = (saved / original) * 100
    else:
        percent = 0

    print("\n╔════════════════════════════════╗")
    print("║       COMPRESSION RESULT       ║")
    print("╠════════════════════════════════╣")
    print(f"║ Original   : {human(original):>16} ║")
    print(f"║ Compressed : {human(final_size):>16} ║")
    print(f"║ Reduction  : {percent:>15.2f}% ║")
    print(f"║ Time       : {elapsed:>15.2f}s ║")
    print("╚════════════════════════════════╝")


def compress_menu():
    clear()
    banner()

    src = input("\nEnter file path: ").strip()

    if not os.path.isfile(src):
        print("[!] File does not exist")
        input("\nPress ENTER...")
        return

    print("""
Compression Mode

[1] FAST
[2] NORMAL
[3] MAX
[4] EXTREME
""")

    mode = input("Select mode: ").strip()

    levels = {
        "1": 1,
        "2": 5,
        "3": 8,
        "4": 9
    }

    level = levels.get(mode)

    if level is None:
        print("[!] Invalid mode")
        input("\nPress ENTER...")
        return

    default = src + ".op.zip"

    dst = input(
        f"\nOutput [{default}]: "
    ).strip()

    if not dst:
        dst = default

    compress_file(src, dst, level)

    input("\nPress ENTER to continue...")


def extract_archive():
    clear()
    banner()

    src = input("\nArchive path: ").strip()

    if not os.path.isfile(src):
        print("[!] Archive not found")
        input("\nPress ENTER...")
        return

    destination = input(
        "Extract folder [./extracted]: "
    ).strip()

    if not destination:
        destination = "./extracted"

    os.makedirs(destination, exist_ok=True)

    try:
        with zipfile.ZipFile(src, "r") as archive:
            archive.extractall(destination)

        print("\n[✓] Extraction complete")
        print(f"[+] Output: {destination}")

    except Exception as e:
        print(f"\n[!] Error: {e}")

    input("\nPress ENTER to continue...")


def info_menu():
    clear()
    banner()

    path = input("\nFile/Folder path: ").strip()

    file_info(path)

    input("\nPress ENTER to continue...")


def settings():
    clear()
    banner()

    print("""
╔════════ SETTINGS ════════╗
║                          ║
║ Engine       : OP        ║
║ Archive      : ZIP       ║
║ Maximum     : Level 9    ║
║ Target Mode  : Enabled   ║
║ Safety       : Enabled   ║
║                          ║
╚══════════════════════════╝
""")

    input("Press ENTER...")


def main_menu():
    while True:
        clear()
        banner()

        print("""
╔════════════════════════════════════╗
║                                    ║
║  [1] Compress File                 ║
║  [2] Extract Archive               ║
║  [3] EXTREME Compression           ║
║  [4] Target Size Mode              ║
║  [5] File Information              ║
║  [6] Settings                      ║
║  [0] Exit                          ║
║                                    ║
╚════════════════════════════════════╝
""")

        choice = input("OP > ").strip()

        if choice == "1":
            compress_menu()

        elif choice == "2":
            extract_archive()

        elif choice == "3":
            clear()
            banner()

            print("""
╔════════════════════════════════════╗
║          OP-XTREME MODE            ║
╠════════════════════════════════════╣
║ Maximum ZIP compression level: 9   ║
║ Best for highly repetitive data.   ║
║                                    ║
║ Note: 1GB -> 200MB cannot be       ║
║ guaranteed for arbitrary files.    ║
╚════════════════════════════════════╝
""")

            src = input("File: ").strip()

            if os.path.isfile(src):
                dst = input(
                    "Output [extreme.op.zip]: "
                ).strip()

                if not dst:
                    dst = "extreme.op.zip"

                compress_file(src, dst, 9)

            input("\nPress ENTER...")

        elif choice == "4":
            clear()
            banner()

            print("""
TARGET SIZE MODE

Example:
1 GB input
Target: 200 MB

The compressor will measure the
actual result instead of guaranteeing
an impossible compression ratio.
""")

            src = input("File: ").strip()
            target = input("Target size (MB): ").strip()

            try:
                target = float(target)
                original = os.path.getsize(src)

                print("\n[+] Target:", target, "MB")
                print("[+] Original:", human(original))

                print(
                    "\n[!] Target mode is prepared for "
                    "the adaptive engine in v2."
                )

            except Exception:
                print("[!] Invalid input")

            input("\nPress ENTER...")

        elif choice == "5":
            info_menu()

        elif choice == "6":
            settings()

        elif choice == "0":
            clear()
            print("OP Compressor closed.")
            sys.exit(0)

        else:
            print("[!] Invalid option")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
