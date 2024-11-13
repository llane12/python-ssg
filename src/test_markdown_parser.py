import unittest
from markdown_parser import *
from textnode import *


class TestMarkdownParser(unittest.TestCase):
    def test_one_block_whitespace(self):
        markdown = "\n   This is normal text with leading and trailing whitespace    \n\n"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "This is normal text with leading and trailing whitespace"
            ],
            blocks)

    def test_three_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block\n* This is a list item\n* This is another list item"""
            ],
            blocks)