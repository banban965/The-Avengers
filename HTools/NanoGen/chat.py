import time

try:
    from database import find_answer, add_answer
except ImportError:
    find_answer = None
    add_answer = None


APP_NAME = "Nano Gen"
MODEL = "GEN-7M"


def normalize(text):
    return " ".join(text.lower().strip().split())


def local_answer(text):
    text = normalize(text)

    if not text:
        return "Please enter a message."

    if find_answer is not None:
        answer = find_answer(text)

        if answer:
            return answer

    basic = {
        "hello": "Hello! I'm Nano Gen.",
        "hi": "Hi! I'm Nano Gen.",
        "سلام": "سلام! من Nano Gen هستم.",
        "help": "Try asking a question or use Command Mode.",
        "who are you": "I'm Nano Gen, model GEN-7M."
    }

    return basic.get(
        text,
        "I don't know the answer yet. You can teach me with Add Answer/Quze."
    )


def normal_response(text):
    return local_answer(text)


def hard_response(text):
    answer = local_answer(text)

    return (
        f"[GEN-7M HARD]\n"
        f"Input : {text}\n"
        f"Answer: {answer}"
    )


def think_response(text):
    print("GEN-7M is thinking...")
    time.sleep(0.5)

    answer = local_answer(text)

    return (
        f"[GEN-7M THINK]\n"
        f"Question: {text}\n"
        f"Result  : {answer}"
    )


def chat(mode="normal"):
    print("╭━━━━━━━━━━━━━━━━━━━━━━╮")
    print("┃      NANO GEN        ┃")
    print(f"┃      {mode.upper():<12}    ┃")
    print("╰━━━━━━━━━━━━━━━━━━━━━━╯")
    print()
    print("Type /exit to return.")
    print()

    while True:
        try:
            user = input("You > ").strip()

        except KeyboardInterrupt:
            print()
            break

        if normalize(user) == "/exit":
            break

        if not user:
            continue

        if mode == "normal":
            answer = normal_response(user)

        elif mode == "hard":
            answer = hard_response(user)

        elif mode == "think":
            answer = think_response(user)

        else:
            answer = normal_response(user)

        print(f"\nBot > {answer}\n")


def normal_chat():
    chat("normal")


def hard_chat():
    chat("hard")


def think_chat():
    chat("think")


if __name__ == "__main__":
    normal_chat()
