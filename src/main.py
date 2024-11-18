import os
import shutil
from html_builder import markdown_to_html_node
from markdown_parser import extract_title
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

def copytree(src, dst, debug=False):
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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from from_path to dest_path using template_path")
    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    output = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    
    with open(dest_path, "w") as file:
        file.write(output)

def main():
    copy_folder_and_all_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
