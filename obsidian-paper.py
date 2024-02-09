import sys
from types import SimpleNamespace
import shutil

import os
import re
import glob

FOLDER_NAME = f"obsidian-paper"
CURRENT_DIR = "/Users/KC/Library/CloudStorage/GoogleDrive-ksuchoi216@gmail.com/My Drive/My Code/ksuchoi216.github.io"
# OBSIDIAN_DIR = "/Users/KC/Library/Mobile\ Documents/iCloud\~md\~obsidian/Documents/FallForward/posts"
OBSIDIAN_DIR = (
    "/Users/KC/Library/Mobile Documents/iCloud~md~obsidian/Documents/FallForward/paper"
)

FOLDER_DIR = f"{CURRENT_DIR}/{FOLDER_NAME}"


def copy_files():
    if not os.path.exists(FOLDER_DIR):
        os.makedirs(FOLDER_DIR)

    paths = glob.glob(f"{OBSIDIAN_DIR}/**")
    # print(f"paths: {paths}")

    folder_paths = []
    for old_path in paths:
        foldername = os.path.basename(old_path)
        new_path = f"{FOLDER_DIR}/{foldername}"
        # print(f"foldername: {foldername}")

        if foldername.endswith(".md"):
            shutil.copy(old_path, new_path)
        else:
            shutil.copytree(old_path, new_path, dirs_exist_ok=True)
            folder_paths.append(new_path)

    return folder_paths


def get_args(args, lines):
    cnt = 0
    tags = []
    for i, line in enumerate(lines):
        if line.strip() == "---":
            cnt += 1
            if cnt == 2:
                args.slice_index = i
                break
        elif line.startswith("date"):
            args.date = re.search(r"date:\s*(\S+)", line).group(1)
        elif line.startswith("category"):
            args.category = re.search(r"category:\s*(\S+)", line).group(1)
        elif line.startswith("  -"):
            tag = re.search(r"\b(\w+)\b", line).group(1)
            tags.append(tag)
        elif line.startswith("title"):
            args.title = re.search(r"title:\s*(.*)", line).group(1)

    args.tags = tags
    # print("tags:", tags)
    lines = lines[args.slice_index + 1 :]
    return args, lines


def modify_lines(args, lines):

    IMG_BASE = f"/images/{args.keyword}"
    if not os.path.exists(f".{IMG_BASE}"):
        os.makedirs(f".{IMG_BASE}")

    args.img_paths = []
    for i, line in enumerate(lines):
        if line.startswith("![["):
            img_file = re.search(r"\[\[(.+?)\]\]", line).group(1)
            img_file = os.path.basename(img_file)

            print(f"img_file: {img_file}")
            old_img_path = f"{args.old_dir}/attachments/{img_file}"
            new_img_path = f"{IMG_BASE}/{img_file}"
            lines[i] = f"![{img_file}]({new_img_path}){{:, .align-center}}\n"
            args.img_paths.append([old_img_path, new_img_path])
            print(f"old_img_path: {old_img_path}, new_img_path: {new_img_path}")

    return args, lines


def _main(args, path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    args, lines = get_args(args, lines)
    args, lines = modify_lines(args, lines)

    new_md_path = f"{CURRENT_DIR}/_posts/-paper.md"
    with open(new_md_path, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    folder_paths = copy_files()

    path = glob.glob(f"{FOLDER_DIR}/paper.md")[0]
    sys.exit()

    args = SimpleNamespace()
    _main(args, path)
