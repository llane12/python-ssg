import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_to_html_raises(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual("HTMLNode(None, None, children=None, None)", repr(node))

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual('', node.props_to_html())

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual('', node.props_to_html())

    def test_props_to_html_values(self):
        props = { "href": "/page.html", "target": "_blank" }
        node = HTMLNode(props=props)
        self.assertEqual(' href="/page.html" target="_blank"', node.props_to_html())


class TestLeafNode(unittest.TestCase):
    def test_to_html_children_None_raises(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is normal text")
        expected = "This is normal text"
        self.assertEqual(expected, node.to_html())
    
    def test_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(expected, node.to_html())

    def test_to_html_a(self):
        node = LeafNode("a", "Click me!", { "href": "https://www.google.com" })
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(expected, node.to_html())


class TestParentNode(unittest.TestCase):
    def test_to_html_children_None_raises(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_children_empty_raises(self):
        node = ParentNode("p", [])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_children_contains_None(self):
        node = ParentNode("p",
            [
                LeafNode(None, "Normal text"),
                None,
                LeafNode("i", "italic text"),
            ])
        expected = "<p>Normal text<i>italic text</i></p>"
        self.assertEqual(expected, node.to_html())

    def test_to_html_one_level(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ])
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(expected, node.to_html())

    def test_to_html_two_levels(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode("a", "Click me!", { "href": "https://www.google.com" })
                ])
            ])
        expected = '<div><p><b>Bold text</b><a href="https://www.google.com">Click me!</a></p></div>'
        self.assertEqual(expected, node.to_html())

    def test_to_html_three_levels(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                "p",
                [
                    ParentNode(
                    "a",
                    [
                        LeafNode(None, "Click me!")
                    ], { "href": "https://www.google.com", "target": "_blank" })
                ])
            ])
        expected = '<div><b>Bold text</b><p><a href="https://www.google.com" target="_blank">Click me!</a></p></div>'
        self.assertEqual(expected, node.to_html())
