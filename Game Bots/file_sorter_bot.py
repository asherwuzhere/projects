# This is the simple file sorter I used to be able to keep all of my projects organized.


import os
import shutil

def sort_python_files(asher_path):
    if not os.path.exists(asher_path):
        print(f"The directory {asher_path} does not exist.")
        return
    
    keywords = ["bot", "ai", "yfinance", "ollama"]
    
    for file in os.listdir(asher_path):
        if file.endswith(".py"):  # Only process Python files
            target_folder = "Other"
            for keyword in keywords:
                if keyword in file.lower():
                    target_folder = keyword.capitalize()
                    break
            
            target_folder_path = os.path.join(asher_path, target_folder)
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)
            
            source = os.path.join(asher_path, file)
            destination = os.path.join(target_folder_path, file)
            shutil.move(source, destination)
            print(f"Moved {file} to {target_folder_path}")

if __name__ == "__main__":
    asher_folder = r"C:\Users\asher"  # Updated to the correct directory path
    sort_python_files(asher_folder)
