from pathlib import Path


# =========================
# APP
# =========================

APP_NAME = "Nano Gen"
MODEL_NAME = "GEN-7M"
VERSION = "1.0.0"


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

ANSWERS_FILE = DATA_DIR / "answers.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
STATS_FILE = DATA_DIR / "stats.json"
DEBUG_LOG_FILE = DATA_DIR / "debug.log"
DEBUG_REPORT_FILE = DATA_DIR / "debug_report.json"


# =========================
# SUPPORTED FILES
# =========================

SUPPORTED_READER_FILES = {
    ".txt",
    ".md",
    ".html",
    ".htm",
    ".pdf"
}


# =========================
# CHAT MODES
# =========================

CHAT_MODES = {
    "1": "normal",
    "2": "hard",
    "3": "think"
}


# =========================
# MAIN MENU
# =========================

MENU_ITEMS = {
    "1": "Normal Chat",
    "2": "Hard Chat",
    "3": "Think Chat",
    "4": "Rish Mode",
    "5": "Termux",
    "6": "Debug Mode",
    "7": "Command Mode",
    "8": "PDF/MD/TXT/HTML Reader",
    "9": "Rish Stats",
    "10": "Add Answer/Quze",
    "11": "All Settings",
    "12": "Exit"
}


# =========================
# UI
# =========================

AUTO_CLEAR_DELAY = 0.3

HEADER_TOP = "╭━━━━━━━━━━━━━━━━━━━━━━╮"
HEADER_MIDDLE = "┃      NANO GEN        ┃"
HEADER_BOTTOM = "╰━━━━━━━━━━━━━━━━━━━━━━╯"


def ensure_directories():
    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def project_info():
    return {
        "name": APP_NAME,
        "model": MODEL_NAME,
        "version": VERSION,
        "directory": str(BASE_DIR),
        "data_directory": str(DATA_DIR)
    }


if __name__ == "__main__":
    ensure_directories()

    print(HEADER_TOP)
    print(HEADER_MIDDLE)
    print(f"┃      {MODEL_NAME:<12}┃")
    print(HEADER_BOTTOM)

    print()
    print("Version :", VERSION)
    print("Project :", BASE_DIR)
    print("Data    :", DATA_DIR)
