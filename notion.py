import argparse
from types import SimpleNamespace
from datetime import datetime
from PIL import Image
import shutil

import os
import re
import glob

BASE_CATEGORIES = ["data-science", "stocks", "book"]
NOTION_DIR = f"./notion"
DOWNLOAD_DIR = "/Users/KC/Downloads"
CURRENT_DIR = "/Users/KC/Library/CloudStorage/GoogleDrive-ksuchoi216@gmail.com/My Drive/My Code/ksuchoi216.github.io"


def move_notion_zip_files(isCopy=False):
    pattern = re.compile(
        r"\b[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}_Export-[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}\b.zip"
    )
    paths = glob.glob(f"{DOWNLOAD_DIR}/*.zip")
    notion_zip_paths = [
        path for path in paths if pattern.match(os.path.relpath(path, DOWNLOAD_DIR))
    ]

    print(notion_zip_paths)

    for notion_zip_path in notion_zip_paths:
        if not os.path.exists(NOTION_DIR):
            os.makedirs(NOTION_DIR)

        if isCopy:
            shutil.copy(notion_zip_path, f"{CURRENT_DIR}/notion")
        else:
            shutil.move(notion_zip_path, f"{CURRENT_DIR}/notion")


def main(base):
    # * get path
    md_path_org = glob.glob(f"{base}/*.md")[0]

    # * markdown
    with open(md_path_org, "r", encoding="utf-8") as file:
        lines = file.readlines()

    keyword = ""  # keyword
    date = ""  # date
    category = ""  # category
    title = ""  # title
    prev_line = ""
    curr_line = ""
    pic_name = ""
    slice_index = 0
    tags = []

    # * get setting variables
    for i, line in enumerate(lines):
        # curr_line = line.strip()
        curr_line = line

        if curr_line.startswith("# "):
            title = re.search(r"# (.*)", curr_line).group(1)
            print("title: ", title)
        elif curr_line.startswith("category"):
            category = re.search(r"category:\s*(\S+)", curr_line).group(1)
            if category not in BASE_CATEGORIES:
                raise ValueError("Invalid category {BASE_CATEGORIES}")
            print("category: ", category)
        elif curr_line.startswith("tags"):
            tags_string = re.search(r"tags:\s*([^\]]*)", curr_line).group(1)
            tags = [tag.strip() for tag in re.split(r"\s*,\s*", tags_string)]
            print("tags:", tags)
        elif curr_line.startswith("date"):
            date = re.search(r"date:\s*(\S+)", curr_line).group(1)
            if len(date) != 8:
                raise ValueError("date should be YYYYMMDD")
            year = int(date[:4])
            month = int(date[4:6])
            day = int(date[6:])
            dt = datetime(year, month, day)
            date = dt.strftime("%Y-%m-%d")
            print("date: ", date)
        elif curr_line.startswith("keyword"):
            keyword = re.search(r"keyword:\s*(\S+)", curr_line).group(1)
            print("keyword: ", keyword)
        elif curr_line.strip() == "---":
            slice_index = i
            print("slice index: ", slice_index)
            break

    # * convert makedown
    img_base_dir = f"/images/{keyword}"

    lines = lines[slice_index + 2 :]

    link_name = ""
    removal_idx = []
    pic_name = ""
    pic_names = []
    for i, line in enumerate(lines):
        # curr_line = line.strip()
        org_line = line
        curr_line = line.strip()
        if curr_line == "---":
            lines[i] = "<!--more-->"

        if curr_line.startswith("!["):  # convert image path
            pic_name = re.search(r"\[([^]]+)\]", curr_line).group(1)
            old_name = re.search(r"\/([^\/]+)\.png", curr_line).group(1)
            if old_name == "Untitled":
                num = 0
            else:
                num = int(old_name[-2:])
            lines[
                i
            ] = f"![{pic_name}]({img_base_dir}/{num:02d}_{pic_name}.png){{:, .align-center}}"
            removal_idx.append(i - 1)
            pic_names.append(pic_name)
            if pic_name == "main":
                lines[i] = ""
                removal_idx.append(i + 1)

        if (curr_line == pic_name) and pic_name != "":  # delete pic_name line
            lines[i] = ""

        if curr_line.startswith("/"):  # get link_name
            link_name = curr_line[1:]
            lines[i] = ""
            removal_idx.append(i + 1)

        if re.search(r"\[https://", curr_line):  # convert link
            url = re.search(r"\(([^)]+)\)", curr_line).group(1)
            lines[i] = f"[{link_name}]({url})\n"

        if org_line != lines[i]:
            print(f"{org_line[:5]} >>>>> {lines[i]}")

    # * remove selected index
    content_lines = [lines[i] for i in range(len(lines)) if i not in removal_idx]

    # * create and move files & folders
    img_path_org = glob.glob(f"{base}/*/*.png")
    img_path_org.insert(
        0, img_path_org.pop(-1)
    )  # move the Untitle.png to first element

    post_base_dir = "./_posts"
    md_path_new = f"{post_base_dir}/{date}-{keyword}.md"

    img_base_dir = f"./{img_base_dir}"
    img_path_org = [f"./{path}" for path in img_path_org]
    img_path_new = [
        f"{img_base_dir}/{num:02d}_{pic_name}.png"
        for num, pic_name in enumerate(pic_names)
    ]

    if not os.path.exists(img_base_dir):
        os.makedirs(img_base_dir)
    else:
        print(f"The image directory already exists: {img_base_dir}")

    for old_path, new_path in zip(img_path_org, img_path_new):
        print(old_path, ">>>img path>>>", new_path)
        shutil.copy(f"{old_path}", f"{new_path}")

    # * rewrite makedown
    start_block = [
        "---\n",
        "excerpt_separator: '<!--more-->'\n",
        f"title: '{title}'\n",
        "categories:\n",
        f"   - {category}\n",
    ]
    tag_block = ["tags:\n"]
    for tag in tags:
        tag = f"   - {tag}\n"
        tag_block.append(tag)

    img_block = [
        "image:\n",
        f"#     path: {img_path_new[0]}\n",
        f"     thumbnail: {img_path_new[0]}\n",
        f"#     caption: \n",
    ]
    end_block = [
        "---\n",
        "\n",
    ]
    base_lines = start_block + tag_block + img_block + end_block
    lines = base_lines + content_lines

    with open(md_path_new, "w") as file:
        file.writelines(lines)


def unpack_zip_files(zip_paths):
    unpack_paths = []
    if zip_paths is not None:
        for i, zip_path in enumerate(zip_paths):
            base_path = f"{NOTION_DIR}/{i}"
            unpack_paths.append(base_path)
            shutil.unpack_archive(zip_path, base_path)

    return unpack_paths


if __name__ == "__main__":
    move_notion_zip_files(isCopy=True)
    zip_paths = glob.glob(f"{NOTION_DIR}/*.zip")
    unpack_paths = unpack_zip_files(zip_paths)
    for unpack_path in unpack_paths:
        print(
            f">>>>>>>>>>>>>>>>>>>>>>>>>> [{unpack_path}] <<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        )
        main(unpack_path)

    try:
        shutil.rmtree(NOTION_DIR)
        print(f"Successfully removed {NOTION_DIR}")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")
