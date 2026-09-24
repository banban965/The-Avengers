from pathlib import Path
import json

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "language": "fa",
    "auto_clear": True,
    "debug": False,
    "theme": "default"
}


def ensure_settings():
    DATA_DIR.mkdir(exist_ok=True)

    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)


def load_settings():
    ensure_settings()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    DATA_DIR.mkdir(exist_ok=True)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            settings,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_setting(name, default=None):
    settings = load_settings()
    return settings.get(name, default)


def set_setting(name, value):
    settings = load_settings()
    settings[name] = value
    save_settings(settings)


def reset_settings():
    save_settings(DEFAULT_SETTINGS.copy())


def show_settings():
    settings = load_settings()

    print("╭──── ALL SETTINGS ────╮")

    for key, value in settings.items():
        print(f"│ {key:<12}: {value}")

    print("╰──────────────────────╯")
