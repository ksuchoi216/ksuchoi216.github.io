
    copy_files(OBSIDIAN_DIR_POSTS)
    paths = glob.glob(f"{FOLDER_DIR}/**")
    for i, path in enumerate(paths):
        args = SimpleNamespace()
        print(f"path: {path}")
        _main(args, path)