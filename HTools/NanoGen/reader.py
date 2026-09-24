from pathlib import Path

try:
    import fitz
except ImportError:
    fitz = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


SUPPORTED = {
    ".txt",
    ".md",
    ".html",
    ".htm",
    ".pdf"
}


def check_file(path):
    file = Path(path).expanduser()

    if not file.exists():
        return False, "File not found."

    if not file.is_file():
        return False, "Path is not a file."

    if file.suffix.lower() not in SUPPORTED:
        return False, "Unsupported file type."

    return True, file


def read_text(file):
    return file.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def read_html(file):
    text = read_text(file)

    if BeautifulSoup:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text("\n", strip=True)

    return text


def read_pdf(file):
    if fitz is None:
        return (
            "PDF support is not installed.\n"
            "Install it with:\n"
            "pip install pymupdf"
        )

    pages = []

    document = fitz.open(str(file))

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)


def read_file(path):
    valid, result = check_file(path)

    if not valid:
        return result

    file = result
    extension = file.suffix.lower()

    if extension == ".pdf":
        return read_pdf(file)

    if extension in [".html", ".htm"]:
        return read_html(file)

    return read_text(file)


def file_info(path):
    valid, result = check_file(path)

    if not valid:
        return result

    file = result

    return {
        "name": file.name,
        "extension": file.suffix.lower(),
        "size": file.stat().st_size,
        "path": str(file)
    }


def print_file(path, limit=10000):
    info = file_info(path)

    if isinstance(info, str):
        print(info)
        return

    print("╭━━━━━━━━ FILE READER ━━━━━━━━╮")
    print(f"┃ Name : {info['name']}")
    print(f"┃ Type : {info['extension']}")
    print(f"┃ Size : {info['size']} bytes")
    print("╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯")

    print()

    content = read_file(path)

    if len(content) > limit:
        content = content[:limit]
        content += "\n\n... [content truncated]"

    print(content)


if __name__ == "__main__":
    path = input("File path > ").strip()

    if path:
        print_file(path)
