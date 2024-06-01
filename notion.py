import glob
import os
import re
import shutil
import sys

import yaml
from easydict import EasyDict as edict


def load_config(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return edict(config)


class NotionHandler:
    def __init__(self, cfg):
        self.cfg = cfg
        self.inotion_dir = cfg.inotion_dir
        self.notion_dir = cfg.notion_dir
        self.post_dir = cfg.post_dir
        self.img_dir = cfg.img_dir
        self.printout = cfg.printout

    def copy_zipfiles(self):
        paths = glob.glob(f"{self.inotion_dir}/*.zip")
        for path in paths:
            shutil.copy(path, self.notion_dir)

    def get_paths(self):
        self.paths = glob.glob(f"{self.notion_dir}/*.zip")
        print(f"paths: {self.paths}") if self.printout else None
        return self.paths

    def unzip(self, path):
        print(f"unzipping {path}") if self.printout else None
        filename = os.path.basename(path).split(".")[0]
        self.unzip_dir = f"{self.notion_dir}/{filename}"
        if not os.path.exists(self.unzip_dir):
            os.makedirs(self.unzip_dir)
        else:
            shutil.rmtree(self.unzip_dir)
        os.system(f"unzip {path} -d {self.unzip_dir}")

    def copy_files(self):
        img_folder = glob.glob(f"{self.unzip_dir}/*/")[0]
        md_path = glob.glob(f"{self.unzip_dir}/*.md")[0]

        # change filename
        self.new_md_path = f"{self.unzip_dir}/index.md"
        shutil.move(md_path, self.new_md_path)

        # change img_folder
        self.new_img_folder = f"{self.unzip_dir}/index_files"
        shutil.move(img_folder, self.new_img_folder)

        img_paths = glob.glob(f"{self.new_img_folder}/*")
        # print(f"img_paths: {img_paths}")
        self.new_img_paths = []
        for img_path in img_paths:
            img_filename = os.path.basename(img_path)
            # find digits from img_filename
            digits = re.search(r"\d+", img_filename)
            if digits is None:
                digits = 0
            else:
                digits = int(digits.group())

            new_img_path = f"{self.new_img_folder}/img_{digits:02d}.png"
            shutil.move(img_path, new_img_path)
            self.new_img_paths.append(new_img_path)

    def modify_lines(self):
        md_path = glob.glob(f"{self.unzip_dir}/*.md")[0]
        print(f"md_path: {md_path}") if self.printout else None
        with open(md_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # * get title firstly
        for line in lines:
            if line.startswith("# "):
                self.title = line[2:].strip()
                print(f"title: {self.title}") if self.printout else None
                break

        # * make save img dir
        self.save_img_dir = f"{self.img_dir}/{self.title}"
        if not os.path.exists(self.save_img_dir):
            os.makedirs(self.save_img_dir)

        new_lines = []
        img_cnt = 0
        line_cnt = 0
        more_idx = 0
        find_content_start_line = False
        save_img_paths = []
        for i, line in enumerate(lines):
            if line.startswith("# "):
                continue

            if line.startswith("date:"):
                date = line.split(":")[1].strip()
                self.date = date.replace("/", "-")
                print(f"date: {self.date}") if self.printout else None
                continue

            if line.startswith("tags:"):
                tags = line.split(":")[1].strip()
                tags = tags.split(",")
                self.tags = [tag.strip() for tag in tags]
                print(f"tags: {self.tags}") if self.printout else None
                continue

            if line.startswith("categories:"):
                self.categories = line.split(":")[1].strip()
                continue

            if line.startswith("done:"):
                continue

            if line.startswith("!["):

                if not find_content_start_line:
                    more_idx = line_cnt - 1
                    find_content_start_line = True

                save_img_path = (
                    f"{self.save_img_dir}/{self.title}_img_{img_cnt:02d}.png"
                )
                save_img_paths.append(save_img_path)
                print(f"save_img_path: {save_img_path[1:]}") if self.printout else None
                line = f"![{self.title}_img_{img_cnt:02d}]({save_img_path[1:]}){{:, .align-center}}\n"
                img_cnt += 1

            new_lines.append(line)
            line_cnt += 1

        more_line = "<!--more-->\n"
        new_lines.insert(more_idx, more_line)

        self.new_lines = new_lines
        self.save_img_paths = save_img_paths

    def create_header_lines(self):
        start_block = [
            "---\n",
            "excerpt_separator: '<!--more-->'\n",
            f"title: '{self.title}'\n",
            "categories:\n",
            f"   - {self.categories}\n",
        ]
        tag_block = ["tags:\n"]
        for tag in self.tags:
            tag = f"    - {tag}\n"
            tag_block.append(tag)

        image_block = [
            "image: \n",
            f"    path: {self.save_img_paths[0][1:]}\n",
            f"    thumbnail: {self.save_img_paths[0][1:]}\n",
        ]

        end_block = [
            "---\n",
            "\n",
        ]
        self.header_lines = start_block + tag_block + image_block + end_block

    def create_md(self, overwrite=False):
        save_path = f"{self.post_dir}/{self.date}-{self.title}.md"

        if not overwrite:
            if os.path.exists(save_path):
                print(f"file already exists: {save_path}")
                return
        else:
            with open(save_path, "w", encoding="utf-8") as f:
                f.writelines(self.header_lines)
                f.writelines(self.new_lines)

            print(f"created: {save_path}")

    def copy_img_files(self):
        # sort new_img_paths
        self.new_img_paths = sorted(self.new_img_paths)
        self.save_img_paths = sorted(self.save_img_paths)
        print(f"new_img_paths: {self.new_img_paths}")
        print(f"save_img_paths: {self.save_img_paths}")

        for new_img_path, save_img_path in zip(self.new_img_paths, self.save_img_paths):
            shutil.copy(new_img_path, save_img_path)
            print(f"copied: {new_img_path} >>>> {save_img_path}")

    def forward(self):
        self.copy_zipfiles()
        paths = self.get_paths()
        print(f"paths: {paths}") if self.printout else None
        for i, path in enumerate(paths):
            if i >= 1:
                break
            self.unzip(path)
            self.copy_files()
            self.modify_lines()
            self.create_header_lines()
            self.create_md(True)
            self.copy_img_files()


if __name__ == "__main__":
    cfg = load_config("./configs/notion.yaml")

    notion = NotionHandler(cfg)
    notion.forward()
