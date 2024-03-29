import argparse
from types import SimpleNamespace
from datetime import datetime
from PIL import Image

import os


def get_args():
    parser = argparse.ArgumentParser(description="add blog post file")
    parser.add_argument("--date", "-d", help="put yymmdd", type=str)
    parser.add_argument("--keyword", "-k", required=True, help="put keyword", type=str)
    parser.add_argument(
        "--category",
        "-c",
        required=True,
        help="put category",
        type=str,
        default="Time-series",
        choices=["Time-Series", "Stock", "Book"],
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    category = args.category
    if args.keyword is None:
        raise Exception("No Keyword!: put keyword by using -k")
    else:
        keyword = args.keyword

    if args.date is not None:
        dt = args.date
        # if len(dt) != 6:
        # raise print("break")
        year = int("20" + dt[:2])
        month = int(dt[2:4])
        day = int(dt[4:])
        dt = datetime(year, month, day)
        post_date = dt.strftime("%Y-%m-%d")
        # img_date = dt.strftime("%Y%m%d")
    else:
        post_date = datetime.now().strftime("%Y-%m-%d")
        # img_date = datetime.now().strftime("%Y%m%d")

    img_dir = f"./images/{keyword}"
    img_path = os.path.join(img_dir, f"main.jpg")

    # * image
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    else:
        print(f"The image directory already exists: {img_dir}")

    if not os.path.isfile(img_path):
        img = Image.new("RGB", (300, 150))  # (width, height)
        img.save(img_path)
    else:
        print(f"The image already exists: {img_path}")

    # * post
    lines = [
        "---",
        f"title: '{keyword}'",
        "excerpt_separator: '<!--more-->'",
        "categories:",
        f"   - {category}",
        "tags:",
        "   - None",
        "# image:",
        f"#     path: {img_path}",
        f"#     thumbnail: {img_path}",
        f"#     caption: ",
        f"# hidden: true",
        "---",
        "What to learn?, why read?",
        "이 글을 읽는다면 아래 내용을 얻어가게 됩니다.",
        "* ",
        "<!--more-->",
        "## Title",
        "### What? ",
        "### Why? ",
        "### How? ",
        "## 지금까지 배운 것 복습!",
        "## 참고 자료",
    ]
    post_path = os.path.join("./_posts", f"{post_date}-{keyword}.md")

    if not os.path.exists(post_path):
        with open(post_path, "w") as f:
            f.write("\n".join(lines))
    else:
        print(f"The markdown post file already exists: {post_path}")

    # with open(post_path, "w") as f:
    #     f.write("\n".join(lines))
