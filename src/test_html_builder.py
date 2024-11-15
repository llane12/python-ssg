import unittest
from html_builder import *


class TestHtmlBuilder(unittest.TestCase):
    def test_one(self):
        markdown = "# Heading\n\n> A quote\n\n## A list\n\n* Item 1\n* Item 2\n* Item 3\n\n```Some code\nMore code```\n\nNormal text"
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()
        self.assertEqual(html, "<html><body><div><h1>Heading</h1><blockquote>A quote</blockquote><h2>A list</h2><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><pre><code>Some code\nMore code</code></pre><p>Normal text</p></div></body></html>")
    