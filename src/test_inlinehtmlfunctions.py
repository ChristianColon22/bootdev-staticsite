import unittest

from textnode import TextNode, TextType
from inlinemarkdownfunctions import (
    text_node_to_html_node, 
    split_nodes_image, 
    split_nodes_link,
    text_to_textnodes,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)

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
        self.assertDictEqual(html_node.props, {"href": url})

    def test_link(self):
        text = "This is a jill sandwich"
        tag = "img"
        url = "assets/images/jill_sandwich.png"
        node = TextNode(text, TextType.IMAGE, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.value, "")
        self.assertDictEqual(html_node.props, {"src": url, "alt": text})

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

    def test_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_more_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image0](https://i.imgur.com/zjjcJKZ.png)" \
            "and another ![image1](https://imgur.com/gallery/posting-videos-to-imgur-lately-mQqjfWE#/t/coding)" \
            "and one more ![image2](https://imgur.com/gallery/s-not-so-pareto-if-pm-joins-cLschLK#/t/coding)"
        )
        self.assertListEqual(
            [
                ("image0", "https://i.imgur.com/zjjcJKZ.png"),
                ("image1", "https://imgur.com/gallery/posting-videos-to-imgur-lately-mQqjfWE#/t/coding"),
                ("image2", "https://imgur.com/gallery/s-not-so-pareto-if-pm-joins-cLschLK#/t/coding"),
            ],
            matches
        )
    
    def test_single_link(self):
        matches = extract_markdown_links("This is a link to [Google](https://google.com)")
        self.assertListEqual(
            [("Google", "https://google.com") 
            ],
            matches
        )
    

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "This is a link to [Google](https://google.com) and" \
            "This is a link to [Boot.dev](https://boot.dev)."
        )
        self.assertListEqual(
            [
                ("Google", "https://google.com"),
                ("Boot.dev", "https://boot.dev"),
            ],
            matches
        )

    def test_text_to_image(self):
        nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_link(self):
        nodes = [
            TextNode(
                "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT
            ),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_image_edges(self):
        nodes = [
            TextNode(
                "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT
            ),
            TextNode(
                "This is a ![trap](https://imgur.com/gallery/its-trap-LaJ9Kmo)", 
                TextType.IMAGE, "https://imgur.com/gallery/its-trap-LaJ9Kmo"
            ),
            TextNode(
                "What does he look like?![Mace](https://imgur.com/gallery/15-mace-windu-memes-rCkwCex#/t/star_wars)",
                TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(
                    "This is a ![trap](https://imgur.com/gallery/its-trap-LaJ9Kmo)", 
                    TextType.IMAGE, "https://imgur.com/gallery/its-trap-LaJ9Kmo"
                ),
                TextNode("What does he look like?", TextType.TEXT),
                TextNode("Mace", TextType.IMAGE, "https://imgur.com/gallery/15-mace-windu-memes-rCkwCex#/t/star_wars")
            ],
            new_nodes,
        )

    def test_text_to_link_edges(self):
        nodes = [
            TextNode(
                "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT
            ),
            TextNode(
                "This is a [trap](https://imgur.com/gallery/its-trap-LaJ9Kmo)", 
                TextType.LINK, "https://imgur.com/gallery/its-trap-LaJ9Kmo"
            ),
            TextNode(
                "What does he look like?[Mace](https://imgur.com/gallery/15-mace-windu-memes-rCkwCex#/t/star_wars)",
                TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(
                    "This is a [trap](https://imgur.com/gallery/its-trap-LaJ9Kmo)", 
                    TextType.LINK, "https://imgur.com/gallery/its-trap-LaJ9Kmo"
                ),
                TextNode("What does he look like?", TextType.TEXT),
                TextNode("Mace", TextType.LINK, "https://imgur.com/gallery/15-mace-windu-memes-rCkwCex#/t/star_wars")
            ],
            new_nodes,
        )
    

    def test_text_to_textnode(self):
        in_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(in_text)
        )
