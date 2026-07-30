# This is the simple file sorter I used to be able to keep all of my projects organized.


import argparse
from pathlib import Path
import shutil

def sort_python_files(directory):
    directory = Path(directory).expanduser().resolve()
    if not directory.is_dir():
        raise NotADirectoryError(f"The directory {directory} does not exist.")
    
    keywords = ["bot", "ai", "yfinance", "ollama"]
    
    for source in directory.iterdir():
        if source.is_file() and source.suffix.lower() == ".py":
            target_folder = "Other"
            for keyword in keywords:
                if keyword in source.name.lower():
                    target_folder = keyword.capitalize()
                    break

            target_folder_path = directory / target_folder
            target_folder_path.mkdir(exist_ok=True)
            destination = target_folder_path / source.name
            if destination.exists():
                print(f"Skipped {source.name}: {destination} already exists.")
                continue
            shutil.move(source, destination)
            print(f"Moved {source.name} to {target_folder_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort Python files into category folders.")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to organize")
    sort_python_files(parser.parse_args().directory)
