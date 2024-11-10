import unittest
from parser import *
from textnode import *


class TestParser(unittest.TestCase):
    def test_no_closing_italic_raises_value_error(self):
        node = TextNode("This is text with an opening *italic marker, but no closing marker", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "*", TextType.ITALIC)

    def test_non_text_nodes_are_just_returned(self):
        bold_node = TextNode("Bold text", TextType.BOLD)
        italic_node = TextNode("Italic text", TextType.ITALIC)
        code_node = TextNode("Some code", TextType.CODE)
        new_nodes = split_nodes_delimiter([bold_node, italic_node, code_node], "`", TextType.CODE)
        self.assertEqual(3, len(new_nodes))

    def test_bold_inside_text(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)        
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes)

    def test_code_inside_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes)
        
    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_italic_at_start_of_text(self):
        node = TextNode("*Italic text* at the start of a sentence.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Italic text", TextType.ITALIC),
                TextNode(" at the start of a sentence.", TextType.TEXT)
            ],
            new_nodes)

    def test_markdown_image_parser(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            images)
        
    def test_markdown_link_parser(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            links)


if __name__ == "__main__":
    unittest.main()
