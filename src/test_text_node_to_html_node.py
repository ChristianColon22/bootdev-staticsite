import unittest

from textnode import TextNode, TextType
from converterfunctions import text_node_to_html_node

class TextTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        text = "This is a bold text node"
        tag = "b"
        url = None
        node = TextNode(text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.value, text)


    def test_italic(self):
        text = "This is a italic text node"
        tag = "i"
        url = None
        node = TextNode(text, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.value, text)

    def test_code(self):
        text = "This is a code text node"
        tag = "code"
        url = None
        node = TextNode(text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.value, text)

    def test_link(self):
        text = "This is a link text node"
        tag = "a"
        url = "https://google.com"
        node = TextNode(text, TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.props, {"href": url})

    def test_link(self):
        text = "This is a jill sandwich"
        tag = "img"
        url = "assets/images/jill_sandwich.png"
        node = TextNode(text, TextType.IMAGE, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": url, "alt": text})
