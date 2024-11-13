import unittest
from inline_markdown_parser import *
from textnode import *


class TestInlineMarkdownParser(unittest.TestCase):
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

    # def test_markdown_image_parser(self):
    #     text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #     images = extract_markdown_images(text)
    #     self.assertListEqual(
    #         [
    #             ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
    #             ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
    #         ],
    #         images)
        
    # def test_markdown_link_parser(self):
    #     text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #     links = extract_markdown_links(text)
    #     self.assertListEqual(
    #         [
    #             ("to boot dev", "https://www.boot.dev"),
    #             ("to youtube", "https://www.youtube.com/@bootdotdev")
    #         ],
    #         links)
        
    def test_split_images_one(self):
        node = TextNode(
            "Text with ![an image](https://i.imgur.com/aKaOqIh.gif)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            ],
            new_nodes)
    
    def test_split_images_two(self):
        node = TextNode(
            "This is text with ![image 1](https://i.imgur.com/aKaOqIh.gif) and ![image 2](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("image 1", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image 2", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            new_nodes)
        
    def test_split_images_two_no_additional_text(self):
        node = TextNode(
            "![image 1](https://i.imgur.com/aKaOqIh.gif)![image 2](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image 1", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode("image 2", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            new_nodes)
        
    # def test_split_links_invalid_syntax(self):
    #     node = TextNode("Text with[a [link](https://www.boot.dev)", TextType.TEXT)
    #     self.assertRaises(ValueError, split_nodes_link, [node])
        
    def test_split_links_one(self):
        node = TextNode(
            "Text with[a link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes)

    def test_split_links_two(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes)
        
    def test_split_links_no_additional_text(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)[YouTube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("YouTube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes)
        
    def test_all_markdown_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            nodes)


if __name__ == "__main__":
    unittest.main()
