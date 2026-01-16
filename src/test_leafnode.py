import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Visit Boot.dev", {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.to_html(),  "<a href=\"https://boot.dev\" target=\"_blank\">Visit Boot.dev</a>")

