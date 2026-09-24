from browser.via import ViaBrowser
from browser.history import History
from browser.bookmarks import Bookmarks
from config import APP_NAME, VERSION


def show_banner():
    print()
    print("╔══════════════════════════════════════╗")
    print("║              ⚡ THOR                 ║")
    print("║           THOR BROWSER               ║")
    print(f"║              v{VERSION}              ║")
    print("╚══════════════════════════════════════╝")


def show_menu():
    print()
    print("[1] Open URL")
    print("[2] Search Web")
    print("[3] History")
    print("[4] Bookmarks")
    print("[5] Add Bookmark")
    print("[6] Remove Bookmark")
    print("[7] Clear History")
    print("[0] Exit")
    print()


def show_history(history):
    items = history.get_all()

    print()
    print("========== HISTORY ==========")

    if not items:
        print("No history found.")
        return

    for index, url in enumerate(items, 1):
        print(f"{index:02d}. {url}")


def show_bookmarks(bookmarks):
    items = bookmarks.get_all()

    print()
    print("======== BOOKMARKS ==========")

    if not items:
        print("No bookmarks found.")
        return

    for index, url in enumerate(items, 1):
        print(f"{index:02d}. {url}")


def main():
    browser = ViaBrowser()
    history = History()
    bookmarks = Bookmarks()

    show_banner()

    while True:
        show_menu()

        choice = input("Thor > ").strip()

        if choice == "1":
            url = input("URL > ").strip()

            if browser.open(url):
                print("[Thor] Opening URL...")
            else:
                print("[Thor] Failed to open URL.")

        elif choice == "2":
            query = input("Search > ").strip()

            if browser.search(query):
                print("[Thor] Opening search...")
            else:
                print("[Thor] Search failed.")

        elif choice == "3":
            show_history(history)

            open_choice = input(
                "\nOpen history item? [Y/N] > "
            ).strip().lower()

            if open_choice == "y":
                number = input("Number > ").strip()

                if number.isdigit():
                    index = int(number) - 1
                    items = history.get_all()

                    if 0 <= index < len(items):
                        browser.open(items[index])
                    else:
                        print("[Thor] Invalid number.")

        elif choice == "4":
            show_bookmarks(bookmarks)

            open_choice = input(
                "\nOpen bookmark? [Y/N] > "
            ).strip().lower()

            if open_choice == "y":
                number = input("Number > ").strip()

                if number.isdigit():
                    index = int(number) - 1
                    items = bookmarks.get_all()

                    if 0 <= index < len(items):
                        browser.open(items[index])
                    else:
                        print("[Thor] Invalid number.")

        elif choice == "5":
            url = input("Bookmark URL > ").strip()
            url = browser.normalize(url)

            if url:
                if bookmarks.add(url):
                    print("[Thor] Bookmark added.")
                else:
                    print("[Thor] Bookmark already exists.")
            else:
                print("[Thor] Invalid URL.")

        elif choice == "6":
            show_bookmarks(bookmarks)

            number = input(
                "\nBookmark number to remove > "
            ).strip()

            if number.isdigit():
                index = int(number) - 1
                items = bookmarks.get_all()

                if 0 <= index < len(items):
                    bookmarks.remove(items[index])
                    print("[Thor] Bookmark removed.")
                else:
                    print("[Thor] Invalid number.")

        elif choice == "7":
            confirm = input(
                "Clear all history? [Y/N] > "
            ).strip().lower()

            if confirm == "y":
                history.clear()
                print("[Thor] History cleared.")

        elif choice == "0":
            print("[Thor] Goodbye.")
            break

        else:
            print("[Thor] Invalid option.")


if __name__ == "__main__":
    main()
