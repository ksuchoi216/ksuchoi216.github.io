import glob
import os
import re
import shutil
import sys
from types import SimpleNamespace


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


def copy_dir(dir_from, dir_to):

    if not os.path.exists(dir_to):
        os.makedirs(dir_to)

    paths = glob.glob(f"{dir_from}/*.md")
    for path in paths:
        shutil.copy(path, dir_to)

    print(f"test")


DIR_FORM = (
    "/Users/KC/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian/papers"
)
CURRENT_DIR = "/Users/KC/Library/CloudStorage/GoogleDrive-ksuchoi216@gmail.com/My Drive/ksuchoi216.github.io"
DIR_TO = f"{CURRENT_DIR}/obsidian_temp"


if __name__ == "__main__":
    copy_dir(DIR_FORM, DIR_TO)
