import os 
import shutil 

def copy_files_recursive(src_path, dest_path):
    src_path = os.path.abspath(src_path)
    dest_path = os.path.abspath(dest_path)
    # If source directory doesn't exist, exit with error
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"{src_path} directory not found.")
    # If destination path doesn't exist, create it
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    # Iterate over contents of source path
    for item in os.listdir(src_path):
        full_path = os.path.join(src_path, item)
        if os.path.isfile(full_path):
            print(f"Copying a file at path {full_path}")
            shutil.copy(full_path, os.path.join(dest_path, item))
        elif os.path.isdir(full_path):
            print(f"Copying a directory at path {full_path}")
            # Create a copy at the destination
            dest_copy_dir = os.path.join(dest_path, item)
            os.makedirs(dest_copy_dir, exist_ok=True)
            # Recursive call to copy contents of this dir to new dir
            copy_files_recursive(full_path, dest_copy_dir)
        else: 
            print(f"Skipping unsupported file type: {full_path}")

