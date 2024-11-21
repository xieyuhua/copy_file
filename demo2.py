import os
import shutil
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Define the root directory where your files are located
root_directory = 'D:\\Program Files'

# Define the target directory where you want to copy the latest files
target_directory = 'D:\\acopy222'

# Define the file extensions you want to include
file_extensions = ['.txt', '.html', '.docx', '.pdf', '.zip', '.ppt']  # Add more extensions as needed



def copy_file(source, destination):
    """复制文件到指定目的地，并打印成功消息。"""
    try:
        shutil.copy2(source, destination)
        # print(f"Successfully copied {source} to {destination}.")
    except PermissionError as e:
        print(f"Failed to copy {source} to {destination}: {e}")
    except Exception as e:
        print(f"An error occurred while copying {source}: {e}")

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
    使用线程池将每个格式的最新文件复制到目标目录下的对应格式子目录中。
    
    :param all_files: 包含按格式分类的文件路径的字典。
    :param target_dir: 目标目录的路径。
    :param max_workers: 线程池中的最大工作线程数。
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        
        for file_name, file_paths in all_files.items():
            ext = file_name.split('.')[-1].lower()
            # 为该格式创建一个子目录
            format_dir = os.path.join(target_dir, ext)
            if not os.path.exists(format_dir):
                os.makedirs(format_dir, exist_ok=True)

            # 找到并复制最新文件
            latest_file = get_latest_file(file_paths)
            destination = os.path.join(format_dir, os.path.basename(latest_file))

            # 提交复制任务到线程池
            futures.append(executor.submit(copy_file, latest_file, destination))
        
        #可选：等待所有任务完成（如果需要的话）
        for future in futures:
            future.result()  # 这会阻塞直到所有任务完成

# Collect all files that match the specified extensions
all_files = collect_files(root_directory, file_extensions)

# Copy the latest files to the target directory
copy_latest_files(all_files, target_directory)

