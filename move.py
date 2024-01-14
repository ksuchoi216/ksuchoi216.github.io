import os
import glob
import re
import shutil

DOWNLOAD_DIR = "/Users/KC/Downloads"
CURRENT_DIR = "/Users/KC/Library/CloudStorage/GoogleDrive-ksuchoi216@gmail.com/My Drive/My Code/ksuchoi216.github.io"

if __name__ == "__main__":
    pattern = re.compile(
        r"\b[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}_Export-[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}\b.zip"
    )
    paths = glob.glob(f"{DOWNLOAD_DIR}/*.zip")
    notion_zip_paths = [
        path for path in paths if pattern.match(os.path.relpath(path, DOWNLOAD_DIR))
    ]

    print(notion_zip_paths)

    for notion_zip_path in notion_zip_paths:
        if os.path.exists(notion_zip_path):
            shutil.move(notion_zip_path, f"{CURRENT_DIR}/notion")
    # move files
