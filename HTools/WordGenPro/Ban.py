import random
import string
import sys

CHARS = string.ascii_letters + string.digits

def create_wordlist(count, length, filename):
    with open(filename, "w") as f:
        for _ in range(count):
            password = ''.join(random.choices(CHARS, k=length))
            f.write(password + "\n")

print("=== WORDLIST CREATOR ===")
print("Characters: A-Z a-z 0-9")

try:
    count = int(input("Count: "))
    length = int(input("Length: "))
    filename = input("Output file [wordlist.txt]: ").strip()

    if not filename:
        filename = "wordlist.txt"

    if count <= 0 or length <= 0:
        raise ValueError

    print("\nCreating...")
    create_wordlist(count, length, filename)

    print(f"\nDone!")
    print(f"File   : {filename}")
    print(f"Lines  : {count}")
    print(f"Length : {length}")

except ValueError:
    print("Invalid input.")
    sys.exit(1)
