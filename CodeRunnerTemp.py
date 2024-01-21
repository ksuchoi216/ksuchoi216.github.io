    try:
        shutil.rmtree(NOTION_DIR)
        print(f"Successfully removed {NOTION_DIR}")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")