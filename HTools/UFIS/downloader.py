import requests
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from merge import merge_parts


def get_size(url):
    try:
        r = requests.head(url, timeout=10)
        return int(r.headers.get("content-length", 0))
    except:
        return 0


def download_part(url, start, end, filename, part, progress, task):

    headers = {
        "Range": f"bytes={start}-{end}"
    }

    try:
        r = requests.get(
            url,
            headers=headers,
            stream=True,
            timeout=20
        )

        with open(f"{filename}.part{part}", "wb") as f:

            for chunk in r.iter_content(
                chunk_size=1024 * 64
            ):

                if chunk:
                    f.write(chunk)

                    progress.update(
                        task,
                        advance=len(chunk)
                    )

        print(f"Part {part} completed")

    except Exception as e:
        print(
            f"Part {part} error:",
            e
        )


def multi_download(url, filename, threads=4):

    size = get_size(url)

    if size == 0:
        print(
            "Cannot detect file size"
        )
        return


    print(
        f"File size: {size / 1024 / 1024:.2f} MB"
    )


    chunk = size // threads

    jobs = []


    for i in range(threads):

        start = i * chunk

        end = start + chunk - 1


        if i == threads - 1:
            end = size - 1


        jobs.append(
            (
                url,
                start,
                end,
                filename,
                i
            )
        )


    columns = [
        TextColumn(
            "[progress.description]{task.description}"
        ),
        BarColumn(),
        TextColumn(
            "{task.percentage:>3.1f}%"
        ),
        TimeRemainingColumn()
    ]


    with Progress(*columns) as progress:

        task = progress.add_task(
            "Downloading",
            total=size
        )


        with ThreadPoolExecutor(
            max_workers=threads
        ) as executor:


            for job in jobs:

                executor.submit(
                    download_part,
                    *job,
                    progress,
                    task
                )


    print(
        "\nMerging files..."
    )

    merge_parts(
        filename,
        threads
    )


    print(
        "\nDownload completed!"
    )