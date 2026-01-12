import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_defaults(self):
        node = HTMLNode()
        actual = [node.tag, node.value, node.children, node.props]
        expected = [None] * 4
        self.assertEqual(actual, expected)


    def test_props_to_html(self):
        props = {
                "href": "https://google.com",
                "target": "_blank",
                "style": "{color: red}"
        }
        node = HTMLNode("a", "Google", [], props)
        actual = node.props_to_html()
        expected = " href=\"https://google.com\" target=\"_blank\" style=\"{color: red}\""
        self.assertEqual(actual, expected)

    def test_repr(self):
        node = HTMLNode("h1", "This is a header")
        self.assertEqual(repr(node), "HTMLNode(h1, This is a header, None, None)")

    def test_children(self):
        child = HTMLNode("h2", "Oldest")
        child2 = HTMLNode("h3", "Youngest")
        prop_dict = {"a_prop": "a_value"}
        node = HTMLNode("h1", "Parent", [child, child2], prop_dict)
        exp = f"HTMLNode(h1, Parent, [HTMLNode(h2, Oldest, None, None), HTMLNode(h3, Youngest, None, None)], {prop_dict})"
        self.assertEqual(repr(node), exp)
