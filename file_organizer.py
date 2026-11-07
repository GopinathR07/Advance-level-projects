
from pathlib import Path
import shutil


# 1. File extension to folder mapping
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Programs": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
}


# 2. Identify the category of a file
def get_category(file_path):

    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            return category

    return "Others"


# 3. Find a safe destination filename
def get_unique_path(destination):

    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix

    counter = 1

    while True:

        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1


# 4. Organize files
def organize_files(folder_path, dry_run=True):

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print("Invalid folder path!")
        return

    files = [item for item in folder.iterdir() if item.is_file()]

    if not files:
        print("No files found in this folder.")
        return

    print("\n===== FILE ORGANIZER =====")

    moved_count = 0

    for file_path in files:

        category = get_category(file_path)

        target_folder = folder / category
        destination = target_folder / file_path.name

        destination = get_unique_path(destination)

        if dry_run:

            print(
                f"[DRY RUN] {file_path.name} "
                f"-> {category}/{destination.name}"
            )

        else:

            try:

                target_folder.mkdir(
                    parents=True,
                    exist_ok=True
                )

                shutil.move(
                    str(file_path),
                    str(destination)
                )

                print(
                    f"Moved: {file_path.name} "
                    f"-> {category}/{destination.name}"
                )

                moved_count += 1

            except OSError as error:

                print(f"Could not move {file_path.name}: {error}")

    if dry_run:
        print("\nDry run completed. No files were moved.")
        print("Set dry_run=False to perform the actual moves.")

    else:
        print(f"\nSuccessfully organized {moved_count} files.")


# 5. Main function
def main():

    print("===== AUTOMATED FILE ORGANIZER =====")

    folder_path = input(
        "Enter the folder path to organize: "
    ).strip().strip('"')

    organize_files(
        folder_path,
        dry_run=False
    )


if __name__ == "__main__":
    main()
