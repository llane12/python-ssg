from textnode import *
from htmlnode import *


class Converter:
    def text_node_to_html_node(self, text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, { "href": text_node.url })
            case TextType.IMAGE:
                return LeafNode("img", None, { "alt": text_node.text, "href": text_node.url })
            case _:
                raise ValueError(f"Unsupported TextType {text_node.text_type}")
