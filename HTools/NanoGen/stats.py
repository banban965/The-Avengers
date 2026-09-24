from pathlib import Path
import json
import platform
import subprocess
import time

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
STATS_FILE = DATA_DIR / "stats.json"

DEFAULT_STATS = {
    "messages": 0,
    "questions": 0,
    "answers": 0,
    "commands": 0,
    "rish_commands": 0,
    "files_read": 0,
    "start_time": None
}


def load_stats():
    DATA_DIR.mkdir(exist_ok=True)

    if not STATS_FILE.exists():
        save_stats(DEFAULT_STATS)
        return DEFAULT_STATS.copy()

    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        save_stats(DEFAULT_STATS)
        return DEFAULT_STATS.copy()


def save_stats(stats):
    DATA_DIR.mkdir(exist_ok=True)

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)


def increment(name, amount=1):
    stats = load_stats()

    if name not in stats:
        stats[name] = 0

    stats[name] += amount
    save_stats(stats)


def set_start_time():
    stats = load_stats()

    if stats["start_time"] is None:
        stats["start_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        save_stats(stats)


def get_rish_stats():
    commands = [
        "id",
        "getprop ro.product.model",
        "getprop ro.build.version.release"
    ]

    results = {}

    for command in commands:
        try:
            result = subprocess.run(
                ["rish", "-c", command],
                capture_output=True,
                text=True,
                timeout=5
            )

            results[command] = (
                result.stdout.strip()
                or result.stderr.strip()
                or "No output"
            )

        except FileNotFoundError:
            results[command] = "rish not found"

        except Exception as e:
            results[command] = str(e)

    return results


def show_stats():
    stats = load_stats()

    print("╭━━━━━━━━ RISH STATS ━━━━━━━━╮")
    print(f"┃ Messages      : {stats['messages']}")
    print(f"┃ Questions     : {stats['questions']}")
    print(f"┃ Answers       : {stats['answers']}")
    print(f"┃ Commands      : {stats['commands']}")
    print(f"┃ Rish Commands : {stats['rish_commands']}")
    print(f"┃ Files Read    : {stats['files_read']}")
    print(f"┃ Started       : {stats['start_time']}")
    print("╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯")


def reset_stats():
    save_stats(DEFAULT_STATS.copy())


if __name__ == "__main__":
    set_start_time()
    show_stats()
