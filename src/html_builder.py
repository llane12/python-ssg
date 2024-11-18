from converter import text_node_to_html_node
from htmlnode import *
from inline_markdown_parser import text_to_textnodes
from markdown_parser import *


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type, values = parse_block(block)
        html_node = markdown_block_to_html_node(block_type, values)
        children.append(html_node)

    return ParentNode("div", children)

def markdown_block_to_html_node(block_type, values):
    match block_type:
        case BlockType.PARAGRAPH:
            child_nodes = []
            for value in values:
                child_nodes.extend(markdown_block_to_child_html_nodes(value))
            return ParentNode("p", child_nodes)
        
        case BlockType.HEADING:
            heading_level = len(values[0])
            return LeafNode(f"h{heading_level}", values[1])
        
        case BlockType.CODE:
            child_nodes = []
            for value in values:
                child_nodes.extend(markdown_block_to_child_html_nodes(value))
            return ParentNode("pre", [ ParentNode("code", child_nodes) ])
        
        case BlockType.QUOTE:
            child_nodes = []
            for value in values:
                child_nodes.extend(markdown_block_to_child_html_nodes(value))
            return ParentNode("blockquote", child_nodes)
        
        case BlockType.UNORDERED_LIST:
            child_nodes = []
            for value in values:
                child_nodes.append(ParentNode("li", markdown_block_to_child_html_nodes(value)))
            return ParentNode("ul", child_nodes)
        
        case BlockType.ORDERED_LIST:
            child_nodes = []
            for value in values:
                child_nodes.append(ParentNode("li", markdown_block_to_child_html_nodes(value)))
            return ParentNode("ol", child_nodes)
        
def markdown_block_to_child_html_nodes(value):
    # Split a Markdown block into a list of inline blocks
    # Convert each Markdown block to a HTML node
    # Then return all the HTML nodes in a list
    return list(map(text_node_to_html_node, text_to_textnodes(value)))
            