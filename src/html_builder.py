from htmlnode import *
from markdown_parser import *


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type, values = parse_block(block)
        children.append(markdown_block_to_html_node(block_type, values))

    return ParentNode("html",
        [
            ParentNode("body", 
            [
                ParentNode("div", children)
            ])
        ])


def markdown_block_to_html_node(block_type, values):
    match block_type:
        case BlockType.PARAGRAPH:
            if len(values) == 1:
                return LeafNode("p", values[0])
            return ParentNode("p", list(map(lambda v: LeafNode(None, v), values)))
        case BlockType.HEADING:
            heading_level = len(values[0])
            return LeafNode(f"h{heading_level}", values[1])
        case BlockType.CODE:
            return ParentNode("pre", [ LeafNode("code", values[0]) ])
        case BlockType.QUOTE:
            return ParentNode("blockquote", list(map(lambda v: LeafNode(None, v), values)))
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", list(map(lambda v: LeafNode("li", v), values)))
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", list(map(lambda v: LeafNode("li", v), values)))
            