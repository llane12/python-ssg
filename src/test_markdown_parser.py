import unittest
from markdown_parser import *
from textnode import *


class TestMarkdownToBlocks(unittest.TestCase):
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

class TestBlockToBlockType(unittest.TestCase):
    # Input should be stripped of whitespace
    def test_paragraph_type(self):
        block = "This is normal text"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_valid_heading_one(self):
        block = "# Heading 1"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_valid_heading_three(self):
        block = "### Heading 3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_valid_heading_six(self):
        block = "###### Heading 6"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_invalid_heading_one(self):
        block = "#Heading 1"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_heading_seven(self):
        block = "####### Heading 7"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_valid_code_one_line(self):
        block = "```some code```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)

    def test_valid_code_three_lines(self):
        block = "```some code\nmore code\nlast code```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)

    def test_invalid_code_start(self):
        block = "``some code```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_code_end(self):
        block = "```some code` ``"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_valid_quote_one_line(self):
        block = "> A quote"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_valid_quote_two_lines(self):
        block = "> A quote\n>Over two lines" # No space required after >
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_invalid_quote_two_lines(self):
        block = "> A quote\nOver two lines"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_valid_unordered_list_one_item(self):
        block = "* Item 1"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_valid_unordered_list_three_items(self):
        block = "* Item 1\n- Item 2\n* Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_invalid_unordered_list_one_item(self):
        block = "*Item 1"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_unordered_list_one_item(self):
        block = "-Item 1"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_unordered_list_three_items(self):
        block = "* Item 1\n-Item 2\n* Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_valid_ordered_list_one_item(self):
        block = "1. Item one"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_valid_ordered_list_three_items(self):
        block = "1. Item one\n2. Item two\n3. Item three"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_invalid_ordered_list_one_item_missing_space(self):
        block = "1.Item one"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_ordered_list_one_item_wrong_character(self):
        block = "1,Item one"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_ordered_list_one_item_no_period(self):
        block = "1 Item one"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_ordered_list_one_item_start_at_zero(self):
        block = "0. Item one"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_ordered_list_three_items_missing_space(self):
        block = "1. Item one\n2. Item two\n3.Item three"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_ordered_list_three_items_numbering(self):
        block = "1. Item one\n2. Item two\n2. Item three"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_mixed_block_one(self):
        block = "> Some code\n> More code\n- List item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_mixed_block_two(self):
        block = "- List item\n* List item\n1. Ordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_mixed_block_three(self):
        block = "1. Item one\n2. Item two\n> Some code"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_mixed_block_four(self):
        block = "1. Item one\n2. Item two\n* Item three"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
