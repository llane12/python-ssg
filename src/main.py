import os
import shutil
from textnode import *


def copy_folder_and_all_contents(source, destination):
    if not os.path.exists(source):
        print(f"ERROR Source folder not found: {source}")
        return
    
    if os.path.exists(destination):
        print(f"INFO Destination directory exists, will be deleted: '{destination}'")
        shutil.rmtree(destination)
        print(f"INFO Destination directory deleted successfully: '{destination}'")

    os.makedirs(destination)
    print(f"INFO Destination directory created successfully: '{destination}'")

    copytree(source, destination)

def copytree(src, dst, debug=True):
    names = os.listdir(src)
    for name in names:
        try:
            src_path = os.path.join(src, name)
            dst_path = os.path.join(dst, name)
            if os.path.isdir(src_path):
                if not os.path.exists(dst_path):
                    if debug:
                        print(f"DEBUG creating directory {dst_path}")
                    os.makedirs(dst_path)
                copytree(src_path, dst_path)
            else:
                # Will raise a SpecialFileError for unsupported file types
                if debug:
                    print(f"DEBUG copying {src_path} to {dst_path}")
                shutil.copy2(src_path, dst_path)
        # Catch any error so we can continue with other files
        except Exception as e:
            print(f"ERROR copying {src_path} to {dst_path}: {e}")

def main():
    copy_folder_and_all_contents("static", "public")


if __name__ == "__main__":
    main()
