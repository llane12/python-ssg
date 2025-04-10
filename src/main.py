import os
import shutil
import sys
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
                if debug:
                    print(f"DEBUG copying {src_path} to {dst_path}")
                shutil.copy2(src_path, dst_path)
        # Catch any error so we can continue with other files
        except Exception as e:
            print(f"ERROR copying {src_path} to {dst_path}: {e}")

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path, basepath, debug=False):
    if not os.path.exists(content_dir_path):
        print(f"ERROR Content folder not found: {content_dir_path}")
        return
    
    names = os.listdir(content_dir_path)
    for name in names:
        try:
            src_path = os.path.join(content_dir_path, name)

            if os.path.isdir(src_path):
                dst_path = os.path.join(dest_dir_path, name)
                if not os.path.exists(dst_path):
                    if debug:
                        print(f"DEBUG creating directory {dst_path}")
                    os.makedirs(dst_path)
                generate_pages_recursive(src_path, template_path, dst_path, basepath, debug)
            else:
                if not name.endswith(".md"):
                    continue
                dst_name = name.replace(".md", ".html")
                dst_path = os.path.join(dest_dir_path, dst_name)
                if debug:
                    print(f"DEBUG Generating page {src_path} to {dst_path}")
                generate_page(src_path, template_path, dst_path, basepath, debug)

        # Catch any error so we can continue with other files
        except Exception as e:
            print(f"ERROR Generating page {src_path} to {dst_path}: {e}")

def generate_page(from_path, template_path, dest_path, basepath, debug=True):
    if debug:
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    output = template.replace("{{ Title }}", title).replace("{{ Content }}", content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    with open(dest_path, "w") as file:
        file.write(output)

def main():
    args = sys.argv
    basepath = "/"
    if len(args) > 1:
        basepath = args[1]
    copy_folder_and_all_contents("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath, debug=True)

if __name__ == "__main__":
    main()
