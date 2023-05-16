import shutil
from pathlib import Path


def show_dir_detail(dir: Path):
    print(f"Directory: {dir}")
    if not dir.exists():
        return
    print("Type\tSize\tName")
    for f in dir.iterdir():
        if f.is_dir():
            print("d", end="\t")
        elif f.is_file():
            print("-", end="\t")
        else:
            print("?", end="\t")
        print(f.stat().st_size, end="\t")
        print(f.name)


def remove_dir(dir: Path):
    if dir.exists():
        confirm = input(f"Are you sure to clear {dir}? [y/N] ")
        if confirm.lower() in {"y", "yes", "1"}:
            shutil.rmtree(dir)
