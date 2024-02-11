
        # if line.startswith("![["):
        #     IMG_BASE = f"/images/{keyword}"
        #     img_file = re.search(r"\[\[(.+?)\]\]", line).group(1)
        #     img_file = os.path.basename(img_file)

        #     # print(f"img_file: {img_file}")
        #     old_img_path = f"{args.old_dir}/attachments/{img_file}"
        #     new_img_path = f"{IMG_BASE}/{img_file}"
        #     lines[i] = f"![{img_file}]({new_img_path}){{:, .align-center}}\n"
        #     args.img_paths.append([old_img_path, new_img_path])
        #     # print(f"old_img_path: {old_img_path}, new_img_path: {new_img_path}")
