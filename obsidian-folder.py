import glob
import os
import re
import shutil
import sys
from types import SimpleNamespace

OBSIDIAN_DIR_PAPERS = (
    "/Users/KC/Library/Mobile Documents/iCloud~md~obsidian/Documents/FallForward/papers"
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

    for old_path in paths:
        foldername = os.path.basename(old_path)
        new_path = f"{FOLDER_DIR}/{foldername}"

        try:
            shutil.copytree(old_path, new_path, dirs_exist_ok=True)
        except Exception as e:
            print(e)


def modify_lines(args, lines):
    args.old_dir = f"{OBSIDIAN_DIR_PAPERS}"

    args.img_paths = []
    args.contents = []
    args.titles = []
    args.tags = []
    args.dates = []

    content = []
    title_cnt = 0
    length = len(lines)
    print(f"length: {length}")
    keyword = ""
    cnt = 0
    for i, line in enumerate(lines):
        # print(line)
        _line = line.strip()

        if line.startswith("**"):
            keyword = re.search(r"\*\*(.*?)\*\*", line).group(1)
            print(f"keyword: {keyword}")

        elif line.startswith("- "):
            tags = re.findall(r"#(\w+)", line)
            args.tags.append(tags)
            title = f"[짧은 논문 소개][{keyword}] {line[2:]}"
            args.titles.append(title)

            if title_cnt >= 1:
                print(f"cnt: {cnt}")
                cnt = 0
                content.append("\n")
                args.contents.append(content)
                content = []

            title_cnt += 1

        elif "Main Figure" in line:
            date = re.search(r"\b\d{4}-\d{2}-\d{2}\b", line).group()
            print(f"{title} date: {date}")
            args.dates.append(date)

            # print("line: ", line)
            # line = line.strip()
            IMG_BASE = f"/images/{keyword}"
            img_file = re.search(r"\[\[(.+?)\]\]", line).group(1)
            img_file = os.path.basename(img_file)

            old_img_path = f"{args.old_dir}/attachments/{img_file}"
            new_img_path = f"{IMG_BASE}/{img_file}"
            lines[i] = f"![{img_file}]({new_img_path}){{:, .align-center}}\n"
            args.img_paths.append([old_img_path, new_img_path])
            # print(f"old_img_path: {old_img_path}, new_img_path: {new_img_path}")
            content.append(f"{lines[i]}\n")
        else:
            print(f"content: {i}")
            if _line.endswith("?"):
                _line = f"\n## {_line[2:]}\n"
            else:
                _line = f"- {_line[2:]}\n"
            cnt += 1
            content.append(_line)

        if i == length - 1 or _line.startswith("---"):
            args.contents.append(content)
            break

        print(f"{i}: {line}")
    return args, lines


def create_markdown(args, i, title, contents, date, tags):
    start_block = [
        "---\n",
        "excerpt_separator: '<!--more-->'\n",
        f"title: '{title}'\n",
        "categories:\n",
        f"   - paper\n",
    ]
    tag_block = ["tags:\n"]
    for tag in tags:
        tag = f"   - {tag}\n"
        tag_block.append(tag)
    # print(f"args.img_paths: {args.img_paths}")
    end_block = [
        "---\n",
        "\n",
        "<!--more-->\n",
    ]
    base_lines = start_block + tag_block + end_block
    lines = base_lines + contents

    new_md_path = f"./_posts/{date}-paper{i:02d}.md"
    with open(new_md_path, "w") as f:
        f.writelines(lines)


def _main(args, path):
    args.old_md_path = path
    with open(args.old_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    args, lines = modify_lines(args, lines)
    # print(args.titles)

    for old_img_path, new_img_path in args.img_paths:
        img_folder_dir = os.path.dirname(new_img_path)
        if not os.path.exists(f".{img_folder_dir}"):
            os.makedirs(f".{img_folder_dir}")
        # print(f"{old_img_path}", ">>>>>>", new_img_path)
        shutil.copy(f"{old_img_path}", f".{new_img_path}")

    print(
        f"titles, contents, dates = {len(args.titles)}, {len(args.contents)}, {len(args.dates)}"
    )

    if len(args.titles) != len(args.contents) or len(args.titles) != len(args.dates):
        print("Check the length of titles, contents, and dates")
        print(f"args.date: {args.dates}")
        # print(f"args.title: {args.titles}")
        print(f"args.tags: {args.tags}")
        sys.exit()

    for i, (title, content, date, tags) in enumerate(
        zip(args.titles, args.contents, args.dates, args.tags)
    ):
        create_markdown(args, i, title, content, date, tags)

    # sys.exit()


if __name__ == "__main__":
    copy_files(OBSIDIAN_DIR_PAPERS, selected_folder=True)

    # path = glob.glob(f"{FOLDER_DIR}/papers/paper.md")[0]
    path = glob.glob(f"{FOLDER_DIR}/papers/papers.md")[0]
    print(f"path: {path}")
    args = SimpleNamespace()
    _main(args, path)
