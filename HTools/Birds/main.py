#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime

from Engine.scanner import BirdsScanner


VERSION = "2.1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WORDLIST = os.path.join(
    BASE_DIR,
    "Engine",
    "Txt",
    "Common.txt"
)

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "Results"
)

MAX_REQUESTED_THREADS = 9000
MAX_WORKERS = 200

MODES = {
    "1": {
        "name": "Low Speed",
        "threads": 10,
        "timeout": 8,
    },
    "2": {
        "name": "Medium Speed",
        "threads": 25,
        "timeout": 6,
    },
    "3": {
        "name": "Hard Speed",
        "threads": 50,
        "timeout": 5,
    },
    "4": {
        "name": "Super Heavy",
        "threads": 100,
        "timeout": 4,
    },
    "5": {
        "name": "Kingo Heavy",
        "threads": 200,
        "timeout": 3,
    },
}


def clear():
    os.system("clear")


def banner():
    print("""
[==========]
[=== Birds ===]
[=== V2.1.0 ==]
""")


def progress(checked, total):
    if total <= 0:
        return

    width = 30
    ratio = checked / total
    filled = int(width * ratio)

    bar = (
        "█" * filled
        + "░" * (width - filled)
    )

    print(
        f"\r[{bar}] "
        f"{ratio * 100:6.2f}% "
        f"{checked}/{total}",
        end="",
        flush=True,
    )


def main():
    clear()
    banner()

    if not os.path.isfile(WORDLIST):
        print("[!] Wordlist not found:")
        print(f"    {WORDLIST}")
        sys.exit(1)

    target = input(
        "Site Url :\n> "
    ).strip()

    if not target.startswith(
        ("http://", "https://")
    ):
        print(
            "[!] URL must start with "
            "http:// or https://"
        )
        return

    print("""
Select Mode

1. Low Speed
2. Medium Speed
3. Hard Speed
4. Super Heavy
5. Kingo Heavy
""")

    mode = input(
        "/.Select :\n> "
    ).strip()

    if mode not in MODES:
        print("[!] Invalid mode.")
        return

    selected = MODES[mode]

    requested = input(
        f"\nThreads [default "
        f"{selected['threads']}] :\n> "
    ).strip()

    if requested:
        try:
            requested_threads = int(requested)
        except ValueError:
            print("[!] Threads must be a number.")
            return

        if not 1 <= requested_threads <= MAX_REQUESTED_THREADS:
            print(
                f"[!] Threads must be between "
                f"1 and {MAX_REQUESTED_THREADS}."
            )
            return
    else:
        requested_threads = selected["threads"]

    actual_workers = min(
        requested_threads,
        MAX_WORKERS
    )

    print()
    print("================================")
    print(f" Birds V{VERSION}")
    print("================================")
    print(f"Target             : {target}")
    print(f"Mode               : {selected['name']}")
    print(f"Requested Threads  : {requested_threads}")
    print(f"Actual Workers     : {actual_workers}")
    print(f"Wordlist           : {WORDLIST}")
    print("================================")
    print()

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    filename = (
        "scan_"
        + datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )
        + ".txt"
    )

    output_file = os.path.join(
        RESULTS_DIR,
        filename
    )

    scanner = BirdsScanner(
        base_url=target,
        wordlist=WORDLIST,
        threads=actual_workers,
        timeout=selected["timeout"],
    )

    def on_result(result, checked, total):
        progress(
            checked,
            total
        )

        print(
            f"\n[{result['status']}] "
            f"{result['url']}"
        )

        try:
            with open(
                output_file,
                "a",
                encoding="utf-8"
            ) as f:
                f.write(
                    f"[{result['status']}] "
                    f"{result['url']}\n"
                )
        except OSError:
            pass

    print("[*] Starting baseline...")
    print("[*] Starting scan...\n")

    start = time.time()

    try:
        result = scanner.scan(
            callback=on_result
        )

    except KeyboardInterrupt:
        print("\n\n[!] Scan stopped.")
        return

    elapsed = time.time() - start

    print("\n")
    print("================================")
    print(" Birds Scan Complete")
    print("================================")
    print(f"Checked : {result['checked']}")
    print(f"Found   : {result['found']}")
    print(f"Errors  : {result['errors']}")
    print(f"Time    : {elapsed:.2f}s")
    print(f"Saved   : {output_file}")
    print("================================")


if __name__ == "__main__":
    main()