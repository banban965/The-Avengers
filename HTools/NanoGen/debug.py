from pathlib import Path
import json
import platform
import sys
import traceback
from datetime import datetime

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOG_FILE = DATA_DIR / "debug.log"


def ensure_data():
    DATA_DIR.mkdir(exist_ok=True)


def log(message, level="INFO"):
    ensure_data()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{timestamp}] [{level}] {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def project_files():
    files = []

    if not BASE_DIR.exists():
        return files

    for path in BASE_DIR.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            files.append(str(path.relative_to(BASE_DIR)))

    return sorted(files)


def check_file(path):
    path = BASE_DIR / path

    return {
        "exists": path.exists(),
        "size": path.stat().st_size if path.exists() else 0
    }


def system_info():
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "system": platform.system(),
        "machine": platform.machine(),
        "architecture": platform.architecture()[0]
    }


def debug_report():
    ensure_data()

    report = {
        "project": "Nano Gen",
        "model": "GEN-7M",
        "time": datetime.now().isoformat(),
        "system": system_info(),
        "files": project_files()
    }

    return report


def show_debug():
    print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
    print("┃     NANO GEN DEBUG   ┃")
    print("┃       GEN-7M         ┃")
    print("╰━━━━━━━━━━━━━━━━━━━━━━╯")

    print("\n[System]")

    info = system_info()

    for key, value in info.items():
        print(f"{key:<12}: {value}")

    print("\n[Project Files]")

    files = project_files()

    if not files:
        print("No files found.")
    else:
        for file in files:
            print(f"  • {file}")

    print(f"\nTotal files: {len(files)}")


def save_report():
    ensure_data()

    report = debug_report()

    report_file = DATA_DIR / "debug_report.json"

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )

    log("Debug report created.")

    return report_file


def safe_call(function, *args, **kwargs):
    try:
        return function(*args, **kwargs)

    except Exception as error:
        log(
            f"{type(error).__name__}: {error}",
            "ERROR"
        )

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            traceback.print_exc(file=f)

        return None


if __name__ == "__main__":
    show_debug()

    print("\nCreating debug report...")

    report = save_report()

    print(f"Report: {report}")
