import unittest
from converter import *
from textnode import *
from htmlnode import LeafNode


class TestConverter(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("Normal text", TextType.TEXT)
        html_node = Converter().text_node_to_html_node(text_node)
        self.assertEqual(None, html_node.tag)
        self.assertEqual("Normal text", html_node.value)
        self.assertEqual(None, html_node.children)
        self.assertEqual(None, html_node.props)

    def test_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = Converter().text_node_to_html_node(text_node)
        self.assertEqual("b", html_node.tag)
        self.assertEqual("Bold text", html_node.value)
        self.assertEqual(None, html_node.children)
        self.assertEqual(None, html_node.props)

    def test_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = Converter().text_node_to_html_node(text_node)
        self.assertEqual("i", html_node.tag)
        self.assertEqual("Italic text", html_node.value)
        self.assertEqual(None, html_node.children)
        self.assertEqual(None, html_node.props)

    def test_code(self):
        text_node = TextNode("Some code", TextType.CODE)
        html_node = Converter().text_node_to_html_node(text_node)
        self.assertEqual("code", html_node.tag)
        self.assertEqual("Some code", html_node.value)
        self.assertEqual(None, html_node.children)
        self.assertEqual(None, html_node.props)

    def test_link(self):
        text_node = TextNode("Click here", TextType.LINK, "/page.html")
        html_node = Converter().text_node_to_html_node(text_node)
        self.assertEqual("a", html_node.tag)
        self.assertEqual("Click here", html_node.value)
        self.assertEqual(None, html_node.children)
        self.assertEqual("/page.html", html_node.props["href"])

    def test_image(self):
        text_node = TextNode("Screenshot", TextType.IMAGE, "/screenshot.png")
        html_node = Converter().text_node_to_html_node(text_node)
        self.assertEqual("img", html_node.tag)
        self.assertEqual(None, html_node.value)
        self.assertEqual(None, html_node.children)
        self.assertEqual("Screenshot", html_node.props["alt"])
        self.assertEqual("/screenshot.png", html_node.props["href"])

    def test_None_text_type_raises_value_error(self):
        text_node = TextNode("Error", None)
        self.assertRaises(ValueError, Converter().text_node_to_html_node, text_node)
    
    def test_unsupported_text_type_raises_value_error(self):
        text_node = TextNode("Error", "INVALID")
        self.assertRaises(ValueError, Converter().text_node_to_html_node, text_node)


if __name__ == "__main__":
    unittest.main()
