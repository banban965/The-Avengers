from rich.console import Console
from rich.panel import Panel

from network import network_info
from dns import dns_optimizer
from optimizer import optimizer
from downloader import multi_download


console = Console()


def banner():
    console.print(
        Panel.fit(
            "[bold cyan]UFNS[/bold cyan]\n"
            "Ultra Fast Network Speed",
            title="v1.0"
        )
    )


def download_menu():
    print("\n=== UFNS Downloader ===")

    url = input("File URL: ")
    filename = input("Save as: ")

    try:
        threads = int(
            input("Threads (default 4): ") or "4"
        )

        multi_download(
            url,
            filename,
            threads
        )

    except Exception as e:
        print("Error:", e)


def menu():

    while True:

        console.print("""
[1] Speed Test
[2] DNS Optimizer
[3] Network Info
[4] Multi Thread Downloader
[5] Network Optimizer
[6] Exit
        """)

        choice = input("UFNS > ")


        if choice == "1":
            console.print(
                "[yellow]Speed Test module coming soon[/yellow]"
            )


        elif choice == "2":
            dns_optimizer()


        elif choice == "3":
            network_info()


        elif choice == "4":
            download_menu()


        elif choice == "5":
            optimizer()


        elif choice == "6":
            print("Exit UFNS...")
            break


        else:
            print("Invalid option")


banner()
menu()