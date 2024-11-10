import re
from textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        found_delim = False
        start = 0
        while True:
            next = node.text.find(delimiter, start)
            if next == -1:
                if found_delim:
                    raise ValueError(f"Invalid syntax: Closing {delimiter} delimiter was not found, for opening at index {start}")
                text = node.text[start:]
                if len(text) > 0:
                    new_nodes.append(TextNode(node.text[start:], TextType.TEXT))
                break
            else:
                text = node.text[start:next]
                if len(text) > 0:
                    new_nodes.append(TextNode(node.text[start:next], text_type if found_delim else TextType.TEXT))
                found_delim = not found_delim
                start = next + len(delimiter)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.+?)\]\((.+?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.+?)\]\((.+?)\)", text)
    return matches
