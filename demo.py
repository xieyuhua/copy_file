import os
import shutil
from collections import defaultdict
from datetime import datetime

def get_latest_file(file_list):
    """
    Get the latest file based on modification time from a list of file paths.
    """
    latest_file = max(file_list, key=os.path.getmtime)
    return latest_file

def collect_files(root_dir, file_extensions):
    """
    Collect all files from the root directory and its subdirectories that match the specified extensions.
    """
    all_files = defaultdict(list)
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Check if the file has one of the specified extensions
            if any(file.lower().endswith(ext) for ext in file_extensions):
                file_path = os.path.join(subdir, file)
                all_files[file].append(file_path)
    return all_files

def copy_latest_files(all_files, target_dir):
    """
    Copy the latest version of each file to the target directory.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    for file_name, file_paths in all_files.items():

        
        ext = file_name.split('.')[-1].lower()
        # 为该格式创建一个子目录
        format_dir = os.path.join(target_dir, ext)
        if not os.path.exists(format_dir):
            os.makedirs(format_dir, exist_ok=True)

        # 找到并复制最新文件
        latest_file = get_latest_file(file_paths)
        try:
            shutil.copy2(latest_file, os.path.join(format_dir, os.path.basename(latest_file)))
            # print(f"Successfully copied {latest_file} to {format_dir}.")
        except PermissionError as e:
            print(f"Failed to copy {latest_file} to {format_dir}: {e}")
        except Exception as e:
            print(f"An error occurred while copying {latest_file}: {e}")
        

# Define the root directory where your files are located
root_directory = 'D:\\Program Files'

# Define the target directory where you want to copy the latest files
target_directory = 'D:\\acopy'

# Define the file extensions you want to include
file_extensions = ['.txt', '.html', '.docx', '.pdf', '.zip', '.ppt']  # Add more extensions as needed

# Collect all files that match the specified extensions
all_files = collect_files(root_directory, file_extensions)

# Copy the latest files to the target directory
copy_latest_files(all_files, target_directory)