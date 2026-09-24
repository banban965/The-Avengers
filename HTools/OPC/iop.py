#!/usr/bin/env python3

import os
import sys
import time
import zipfile


APP = "OP COMPRESSOR PRO"
VERSION = "2.0"


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
║              VERSION 2.0               ║
╠════════════════════════════════════════╣
║       Advanced File & Folder            ║
║             Compression                ║
╚════════════════════════════════════════╝
""")


def folder_info(path):
    total = 0
    count = 0

    for root, dirs, files in os.walk(path):
        for name in files:
            full = os.path.join(root, name)

            try:
                total += os.path.getsize(full)
                count += 1
            except OSError:
                pass

    return total, count


def file_info(path):
    if not os.path.exists(path):
        print("[!] File/Folder not found")
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
        total, count = folder_info(path)

        print("\n╔══════ FOLDER INFO ═══════╗")
        print(f" Name  : {os.path.basename(os.path.abspath(path))}")
        print(f" Files : {count}")
        print(f" Size  : {human(total)}")
        print(f" Path  : {os.path.abspath(path)}")
        print(" Type  : Folder")
        print("╚═══════════════════════════╝")


def show_result(original, compressed, elapsed, count):
    if original > 0:
        reduction = ((original - compressed) / original) * 100
    else:
        reduction = 0

    print("\n╔════════════════════════════════╗")
    print("║       COMPRESSION RESULT       ║")
    print("╠════════════════════════════════╣")
    print(f"║ Files      : {count:<19}║")
    print(f"║ Original   : {human(original):>16} ║")
    print(f"║ Compressed : {human(compressed):>16} ║")
    print(f"║ Reduction  : {reduction:>15.2f}% ║")
    print(f"║ Time       : {elapsed:>15.2f}s ║")
    print("╚════════════════════════════════╝")


def compress_file(src, dst, level):
    if not os.path.isfile(src):
        print("[!] Invalid file")
        return

    original = os.path.getsize(src)

    print("\n[+] OP Engine starting...")
    print(f"[+] Input : {src}")
    print(f"[+] Size  : {human(original)}")
    print(f"[+] Level : {level}")

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
    compressed = os.path.getsize(dst)

    show_result(
        original,
        compressed,
        elapsed,
        1
    )


def compress_folder(src, dst, level):
    if not os.path.isdir(src):
        print("[!] Invalid folder")
        return

    src = os.path.abspath(src)

    original, count = folder_info(src)

    print("\n[+] OP Folder Engine starting...")
    print(f"[+] Input : {src}")
    print(f"[+] Files : {count}")
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

            base = os.path.dirname(src)

            for root, dirs, files in os.walk(src):
                for name in files:

                    full_path = os.path.join(root, name)

                    relative_path = os.path.relpath(
                        full_path,
                        base
                    )

                    try:
                        archive.write(
                            full_path,
                            arcname=relative_path
                        )

                    except OSError as e:
                        print(f"[!] Skipped: {full_path}")
                        print(f"    Reason: {e}")

    except Exception as e:
        print(f"\n[!] Folder compression error: {e}")
        return

    elapsed = time.time() - start
    compressed = os.path.getsize(dst)

    show_result(
        original,
        compressed,
        elapsed,
        count
    )


def compression_mode():
    print("""
Compression Mode

[1] FAST
[2] NORMAL
[3] MAX
[4] EXTREME
""")

    choice = input("Select mode: ").strip()

    levels = {
        "1": 1,
        "2": 5,
        "3": 8,
        "4": 9
    }

    return levels.get(choice)


def compress_file_menu():
    clear()
    banner()

    src = input("\nEnter file path: ").strip()

    if not os.path.isfile(src):
        print("[!] File does not exist")
        input("\nPress ENTER...")
        return

    level = compression_mode()

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


def compress_folder_menu():
    clear()
    banner()

    src = input("\nEnter folder path: ").strip()

    if not os.path.isdir(src):
        print("[!] Folder does not exist")
        input("\nPress ENTER...")
        return

    level = compression_mode()

    if level is None:
        print("[!] Invalid mode")
        input("\nPress ENTER...")
        return

    folder_name = os.path.basename(
        os.path.abspath(src)
    )

    default = folder_name + ".op.zip"

    dst = input(
        f"\nOutput [{default}]: "
    ).strip()

    if not dst:
        dst = default

    compress_folder(src, dst, level)

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
        print(
            f"[+] Output: {os.path.abspath(destination)}"
        )

    except Exception as e:
        print(f"\n[!] Extraction error: {e}")

    input("\nPress ENTER to continue...")


def extreme_mode():
    clear()
    banner()

    print("""
╔════════════════════════════════════╗
║          OP-XTREME MODE            ║
╠════════════════════════════════════╣
║ ZIP compression level: 9           ║
║                                    ║
║ Supports files and folders.        ║
║                                    ║
║ Compression ratio depends on      ║
║ the type of data being compressed.║
╚════════════════════════════════════╝
""")

    print("""
[1] Extreme File
[2] Extreme Folder
[0] Back
""")

    choice = input("Select: ").strip()

    if choice == "1":

        src = input("\nFile: ").strip()

        if not os.path.isfile(src):
            print("[!] File not found")
            input("\nPress ENTER...")
            return

        dst = input(
            "Output [extreme.op.zip]: "
        ).strip()

        if not dst:
            dst = "extreme.op.zip"

        compress_file(src, dst, 9)

        input("\nPress ENTER...")

    elif choice == "2":

        src = input("\nFolder: ").strip()

        if not os.path.isdir(src):
            print("[!] Folder not found")
            input("\nPress ENTER...")
            return

        dst = input(
            "Output [extreme-folder.op.zip]: "
        ).strip()

        if not dst:
            dst = "extreme-folder.op.zip"

        compress_folder(src, dst, 9)

        input("\nPress ENTER...")

    elif choice == "0":
        return

    else:
        print("[!] Invalid option")
        input("\nPress ENTER...")


def target_size_mode():
    clear()
    banner()

    print("""
╔════════════════════════════════════╗
║         TARGET SIZE MODE           ║
╠════════════════════════════════════╣
║                                    ║
║ Target size is an estimate only.  ║
║ ZIP cannot guarantee an arbitrary  ║
║ compression ratio.                ║
║                                    ║
╚════════════════════════════════════╝
""")

    src = input("File/Folder: ").strip()
    target = input("Target size (MB): ").strip()

    try:
        target = float(target)

        if os.path.isfile(src):
            original = os.path.getsize(src)

        elif os.path.isdir(src):
            original, _ = folder_info(src)

        else:
            print("[!] File/Folder not found")
            input("\nPress ENTER...")
            return

        print(f"\n[+] Target   : {target:.2f} MB")
        print(f"[+] Original : {human(original)}")

        print(
            "\n[!] Adaptive target engine is planned "
            "for a future version."
        )

    except ValueError:
        print("[!] Invalid target size")

    input("\nPress ENTER...")


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
║ Maximum      : Level 9   ║
║ File Mode    : Enabled   ║
║ Folder Mode  : Enabled   ║
║ Extract      : Enabled   ║
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
║  [2] Compress Folder               ║
║  [3] Extract Archive               ║
║  [4] EXTREME Compression           ║
║  [5] Target Size Mode              ║
║  [6] File / Folder Information     ║
║  [7] Settings                      ║
║  [0] Exit                          ║
║                                    ║
╚════════════════════════════════════╝
""")

        choice = input("OP > ").strip()

        if choice == "1":
            compress_file_menu()

        elif choice == "2":
            compress_folder_menu()

        elif choice == "3":
            extract_archive()

        elif choice == "4":
            extreme_mode()

        elif choice == "5":
            target_size_mode()

        elif choice == "6":
            info_menu()

        elif choice == "7":
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
