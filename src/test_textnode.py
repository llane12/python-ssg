import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node1, node2)

    def test_eq_url_default_and_none(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node1, node2)

    def test_eq_url_none(self):
        node1 = TextNode("This is a text node", TextType.ITALIC, None)
        node2 = TextNode("This is a text node", TextType.ITALIC, None)
        self.assertEqual(node1, node2)

    def test_eq_url_equal(self):
        node1 = TextNode("This is a text node", TextType.LINK, "/page.html")
        node2 = TextNode("This is a text node", TextType.LINK, "/page.html")
        self.assertEqual(node1, node2)
    
    def test_eq_text_different(self):
        node1 = TextNode("This is a text node", TextType.NORMAL, None)
        node2 = TextNode("This is a different text node", TextType.NORMAL, None)
        self.assertNotEqual(node1, node2)

    def test_eq_text_type_different(self):
        node1 = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.ITALIC, None)
        self.assertNotEqual(node1, node2)
    
    def test_eq_url_different(self):
        node1 = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK, "/page.html")
        self.assertNotEqual(node1, node2)

    def test_eq_url_different_default(self):
        node1 = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK, "")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
