import sys
from types import SimpleNamespace
import shutil

import os
import re
import glob

FOLDER_DIR = f"./obsidian"
CURRENT_DIR = "/Users/KC/Library/CloudStorage/GoogleDrive-ksuchoi216@gmail.com/My Drive/My Code/ksuchoi216.github.io"
OBSIDIAN_DIR = (
    "/Users/KC/Library/Mobile\ Documents/iCloud\~md\~obsidian/Documents/posts"
)


def copy_files():
    paths = glob.glob(f"{OBSIDIAN_DIR}/**")
    print(paths)
    for path in paths:
        if not os.path.exists(FOLDER_DIR):
            os.makedirs(FOLDER_DIR)

        shutil.copy(path, f"{CURRENT_DIR}/notion")


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
    print("tags:", tags)
    lines = lines[args.slice_index :]
    return args, lines


def modify_lines(args, lines):

    IMG_BASE = f"/images/{args.keyword}"
    if not os.path.exists(f".{IMG_BASE}"):
        os.makedirs(f".{IMG_BASE}")

    args.img_paths = []
    for i, line in enumerate(lines):
        if line.startswith("![["):
            img_file = re.search(r"\[\[(.+?)\]\]", line).group(1)
            old_img_path = f"{args.old_dir}/attachments/{img_file}"
            new_img_path = f"{IMG_BASE}/{img_file}"
            lines[i] = f"![{img_file}]({new_img_path}){{:, .align-center}}\n"
            args.img_paths.append([old_img_path, new_img_path])

    return args, lines


def create_blocks(args, lines):
    start_block = [
        "---\n",
        "excerpt_separator: '<!--more-->'\n",
        f"title: '{args.title}'\n",
        "categories:\n",
        f"   - {args.category}\n",
    ]
    tag_block = ["tags:\n"]
    for tag in args.tags:
        tag = f"   - {tag}\n"
        tag_block.append(tag)

    img_block = [
        "image:\n",
        f"     path: {args.img_paths[0][1]}\n",
        f"     thumbnail: {args.img_paths[0][1]}\n",
    ]
    end_block = [
        "---\n",
        "\n",
    ]
    base_lines = start_block + tag_block + img_block + end_block

    lines = base_lines + lines
    return lines


def _main(path):
    args = SimpleNamespace()
    args.old_md_path = glob.glob(f"{path}/*.md")[0]
    args.old_dir = os.path.dirname(args.old_md_path)
    filename = os.path.basename(args.old_md_path)
    args.keyword = re.match(r"(.+?)\.md$", filename).group(1)
    # print(md_path, args.keyword)
    with open(args.old_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    args, lines = get_args(args, lines)
    args, lines = modify_lines(args, lines)

    lines = create_blocks(args, lines)
    for old_img_path, new_img_path in args.img_paths:
        print(f"{old_img_path}", ">>>>>>", new_img_path)
        shutil.copy(f"{old_img_path}", f".{new_img_path}")

    new_md_path = f"./_posts/{args.date}-{args.keyword}.md"
    with open(new_md_path, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    # find folder path using glob
    copy_files()
    paths = glob.glob(f"{FOLDER_DIR}/**")
    for path in paths:
        _main(path)
