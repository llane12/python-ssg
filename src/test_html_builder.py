import unittest
from html_builder import *


class TestHtmlBuilder(unittest.TestCase):
    def test_one(self):
        markdown = "# Heading\n\n> A quote\n\n## A list\n\n* Item 1\n* Item 2\n* Item 3\n\n```Some code\nMore code```\n\nNormal text"
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()
        self.assertEqual(html, "<div><h1>Heading</h1><blockquote>A quote</blockquote><h2>A list</h2><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><pre><code>Some code\nMore code</code></pre><p>Normal text</p></div>")

    def test_two(self):
        markdown = "# Title\n\n1. List item 1 with **bold text**\n2. List item 2 with _some italic_ text inside\n\nA regular paragraph with [a link](/page.html) inside it"
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()
        self.assertEqual(html, '<div><h1>Title</h1><ol><li>List item 1 with <b>bold text</b></li><li>List item 2 with <i>some italic</i> text inside</li></ol><p>A regular paragraph with <a href="/page.html">a link</a> inside it</p></div>')

    def test_code_formatting(self):
        markdown = '# CODE FORMATTING\n\n```\nfunc main(){\n    fmt.Println("Hello, World!")\n}\n```'
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()
        self.assertEqual(html, '<div><h1>CODE FORMATTING</h1><pre><code>func main(){\n    fmt.Println("Hello, World!")\n}</code></pre></div>')

    def test_header_with_inline_markdown(self):
        markdown = '# Heading with some **BOLD** text'
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()
        self.assertEqual(html, '<div><h1>Heading with some <b>BOLD</b> text</h1></div>')

    def test_italic_in_unordered_list(self):
        markdown ='- List item with _italic text_ in it'
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()
        self.assertEqual(html, '<div><ul><li>List item with <i>italic text</i> in it</li></ul></div>')
