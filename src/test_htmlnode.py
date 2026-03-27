import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test2(self):
        node = HTMLNode("h1", "Text Test")
        node2 = HTMLNode("p", "Text Test")
        self.assertNotEqual(node, node2)

    def test3(self):
        test = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        node = HTMLNode("Does this work?", "", [],test)
        node2 = HTMLNode("Does this work?", "", [],test)
        self.assertEqual(node, node2)
    
    def test4(self):
        node = HTMLNode("h1", "Text Test")
        node2 = HTMLNode("h1", "Text Test")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()