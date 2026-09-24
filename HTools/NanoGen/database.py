from pathlib import Path
import json
import re


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_FILE = DATA_DIR / "answers.json"


DEFAULT_ANSWERS = {
    "hello": "Hello! I'm Nano Gen.",
    "hi": "Hi! I'm Nano Gen.",
    "who are you": "I'm Nano Gen, powered by GEN-7M."
}


def normalize(text):
    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def ensure_database():
    DATA_DIR.mkdir(exist_ok=True)

    if not DB_FILE.exists():
        save_database(DEFAULT_ANSWERS)


def load_database():
    ensure_database()

    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {}

        return data

    except (json.JSONDecodeError, OSError):
        save_database(DEFAULT_ANSWERS)
        return DEFAULT_ANSWERS.copy()


def save_database(data):
    DATA_DIR.mkdir(exist_ok=True)

    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_answer(question, answer):
    question = normalize(question)
    answer = str(answer).strip()

    if not question:
        return False, "Question is empty."

    if not answer:
        return False, "Answer is empty."

    database = load_database()

    database[question] = answer

    save_database(database)

    return True, "Answer saved."


def find_answer(question):
    question = normalize(question)

    if not question:
        return None

    database = load_database()

    # Exact match
    if question in database:
        return database[question]

    # Partial match
    for saved_question, answer in database.items():
        if saved_question in question:
            return answer

    return None


def remove_answer(question):
    question = normalize(question)

    database = load_database()

    if question not in database:
        return False

    del database[question]
    save_database(database)

    return True


def get_all_answers():
    return load_database()


def count_answers():
    return len(load_database())


def clear_database():
    save_database({})


def database_info():
    database = load_database()

    return {
        "file": str(DB_FILE),
        "answers": len(database)
    }


if __name__ == "__main__":
    print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
    print("┃   NANO GEN DATABASE  ┃")
    print("┃       GEN-7M         ┃")
    print("╰━━━━━━━━━━━━━━━━━━━━━━╯")

    print()
    print("Database:", DB_FILE)
    print("Answers :", count_answers())

    print("\nTest:")
    print("hello ->", find_answer("hello"))