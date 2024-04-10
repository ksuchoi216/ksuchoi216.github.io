import sys
from types import SimpleNamespace
import shutil

import os
import re
import glob

OBSIDIAN_DIR_POSTS = (
    "/Users/KC/Library/Mobile Documents/iCloud~md~obsidian/Documents/FallForward/ds"
)
CURRENT_DIR = "/Users/KC/Library/CloudStorage/GoogleDrive-ksuchoi216@gmail.com/My Drive/My Code/ksuchoi216.github.io"
FOLDER_NAME = f"obsidian"
FOLDER_DIR = f"{CURRENT_DIR}/{FOLDER_NAME}"


def copy_files(obsidian_dir, selected_folder=False):

    if not os.path.exists(FOLDER_DIR):
        os.makedirs(FOLDER_DIR)

    if selected_folder:
        paths = [f"{obsidian_dir}"]
    else:
        paths = glob.glob(f"{obsidian_dir}/**")

    # print(f"paths: {paths}")
    # sys.exit()
    for old_path in paths:
        foldername = os.path.basename(old_path)
        new_path = f"{FOLDER_DIR}/{foldername}"

        try:
            shutil.copytree(old_path, new_path, dirs_exist_ok=True)
        except Exception as e:
            print(e)


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
    # print(f'args.slice_index: {args.slice_index}')
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

            # print(f"img_file: {img_file}")
            old_img_path = f"{args.old_dir}/attachments/{img_file}"
            new_img_path = f"{IMG_BASE}/{img_file}"
            lines[i] = f"![{img_file}]({new_img_path}){{:, .align-center}}\n"
            args.img_paths.append([old_img_path, new_img_path])
            # print(f"old_img_path: {old_img_path}, new_img_path: {new_img_path}")

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
    # print(f"args.img_paths: {args.img_paths}")
    if args.img_paths:
        img_block = [
            "image:\n",
            f"     path: {args.img_paths[0][1]}\n",
            f"     thumbnail: {args.img_paths[0][1]}\n",
        ]
    else:
        img_block = []
    end_block = [
        "---\n",
        "\n",
    ]
    base_lines = start_block + tag_block + img_block + end_block

    lines = base_lines + lines
    return lines


def _main(args, path):
    args.old_md_path = glob.glob(f"{path}/*.md")[0]
    filename = os.path.basename(args.old_md_path)
    args.keyword = re.match(r"(.+?)\.md$", filename).group(1)
    print(f"args.keyword: {args.keyword}")

    args.old_dir = os.path.dirname(args.old_md_path)

    with open(args.old_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    args, lines = get_args(args, lines)

    # sys.exit()
    args, lines = modify_lines(args, lines)

    lines = create_blocks(args, lines)
    for old_img_path, new_img_path in args.img_paths:
        shutil.copy(f"{old_img_path}", f".{new_img_path}")
        # print(f"{old_img_path}", ">>>>>>", new_img_path)

    new_md_path = f"./_posts/{args.date}-{args.keyword}.md"
    with open(new_md_path, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":

    copy_files(OBSIDIAN_DIR_POSTS)
    paths = glob.glob(f"{FOLDER_DIR}/**")
    for i, path in enumerate(paths):
        foldername = os.path.basename(path)
        if foldername in ["papers"]:
            continue

        args = SimpleNamespace()
        # print(f"path: {path}")
        _main(args, path)

    # copy_files(OBSIDIAN_DIR_PAPERS, selected_folder=True)
    # args = SimpleNamespace()
    # _main(args, f"{OBSIDIAN_DIR_PAPERS}")
