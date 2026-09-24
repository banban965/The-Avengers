from pathlib import Path

PROJECT = Path.home() / "NanoGen"

FILES = {
    "main.py": "",
    "config.py": "",
    "database.py": "",
    "chat.py": "",
    "rish.py": "",
    "termux.py": "",
    "debug.py": "",
    "commands.py": "",
    "reader.py": "",
    "stats.py": "",
    "settings.py": "",
    "ui.py": "",
    "data/answers.json": "{}",
    "data/settings.json": """{
    "language": "fa",
    "auto_clear": true,
    "debug": false,
    "theme": "default"
}""",
    "README.md": "# Nano Gen\n\nModel: GEN-7M\n"
}


def create_project():
    print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
    print("┃    NANO GEN BUILDER  ┃")
    print("┃       GEN-7M         ┃")
    print("╰━━━━━━━━━━━━━━━━━━━━━━╯")
    print()

    PROJECT.mkdir(parents=True, exist_ok=True)

    for filename, content in FILES.items():
        path = PROJECT / filename

        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.write_text(content, encoding="utf-8")
            print(f"[+] Created: {filename}")
        else:
            print(f"[=] Exists : {filename}")

    print()
    print("Project created successfully.")
    print(f"Location: {PROJECT}")


if __name__ == "__main__":
    create_project()
