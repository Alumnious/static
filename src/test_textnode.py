import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test3(self):
        node = TextNode("Does this work?", TextType.ITALIC)
        node2 = TextNode("Does this work?", TextType.ITALIC)
        self.assertEqual(node, node2)
    
    def test4(self):
        node = TextNode("Link test", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Link test", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()