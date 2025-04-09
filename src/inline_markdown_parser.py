import re
from textnode import *


def text_to_textnodes(text):
    nodes = [ TextNode(text, TextType.TEXT) ]
    nodes = split_nodes_code(nodes)
    nodes = split_nodes_bold(nodes)
    nodes = split_nodes_italic(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_italic(old_nodes):
    return split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

def split_nodes_bold(old_nodes):
    return split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

def split_nodes_code(old_nodes):
    return split_nodes_delimiter(old_nodes, "`", TextType.CODE)

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

# def split_nodes_regex(old_nodes, regex, text_type):
#     new_nodes = []
#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.append(node)
#             continue

#         matches = re.findall(regex, node.text)
#         if len(matches) == 0:
#             new_nodes.append(node)
#             continue
            
#         for match in matches:
#             if len(match[0]) > 0:
#                 new_nodes.append(TextNode(match[0], TextType.TEXT))
#             new_nodes.append(TextNode(match[1], text_type, match[2]))
#     return new_nodes

# def extract_markdown_images(text):
#     matches = re.findall(r"!\[(.+?)\]\((.+?)\)", text)
#     return matches

# def extract_markdown_links(text):
#     matches = re.findall(r"\[(.+?)\]\((.+?)\)", text)
#     return matches
