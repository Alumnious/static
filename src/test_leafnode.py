import unittest

from htmlnode import *


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img","what do i put here?",{"src":"url/of/image.jpg", "alt":"Description of image"})
        self.assertEqual(node.to_html(), '<img src="url/of/image.jpg" alt="Description of image" />')
    #(self, tag, value, props = None)
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

if __name__ == "__main__":
    unittest.main()