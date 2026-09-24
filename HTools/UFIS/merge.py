import os


def merge_parts(filename, parts):
    print("\n=== UFNS Merge ===")

    with open(filename, "wb") as output:

        for i in range(parts):
            part_file = f"{filename}.part{i}"

            if os.path.exists(part_file):
                with open(part_file, "rb") as part:
                    output.write(part.read())

                os.remove(part_file)

                print(f"Merged part {i}")

            else:
                print(f"Missing: {part_file}")

    print("Merge completed!")