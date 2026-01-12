import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_different_type(self):
        types = [m for m in TextType]
        for i in range(len(types)-1):
            node = TextNode(f"This is {types[i].value}", type[i])
            node2 = TextNode(f"This is {types[i+1].value}", type[i])
            self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.CODE, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.CODE, "https://boot.dev")
        self.assertEqual(node, node2)
    
    def test_not_eq_with_url(self):
        for type in TextType:
            text = f"This is {type.value}"
            node = TextNode(text, type, "link1")
            node2 = TextNode(text, type, "link2")
            self.assertNotEqual(node, node2)
    
    def test_print(self):
        for type in TextType:
            text = "Hello from this unit test"
            url = "https://google.com"
            node = TextNode(text, type, url)
            expected = f"TextNode({text}, {type.value}, {url})"
            self.assertEqual(repr(node), expected)