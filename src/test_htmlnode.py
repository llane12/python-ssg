import unittest

from htmlnode import HTMLNode


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
    