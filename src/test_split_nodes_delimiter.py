import unittest
from converterfunctions import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_bold_block_start(self):
        node = TextNode("**Bold** text this is", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text this is", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_double_italic_start_end(self):
        node = TextNode("_Italic here_ and some _Italic there_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("Italic here", TextType.ITALIC),
            TextNode(" and some ", TextType.TEXT),
            TextNode("Italic there", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_multiple_nodes(self):
        nodes = [
            TextNode("Hi there, I am **bold text**. ", TextType.TEXT),
            TextNode("_Hello there_, I am **a Jedi**. ", TextType.TEXT),
            TextNode("It's a **trap!**", TextType.BOLD)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Hi there, I am ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(". ", TextType.TEXT),
            TextNode("_Hello there_, I am ", TextType.TEXT),
            TextNode("a Jedi", TextType.BOLD),
            TextNode(". ", TextType.TEXT),
            TextNode("It's a **trap!**", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)