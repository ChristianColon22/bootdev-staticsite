from textnode import TextNode, TextType
from leafnode import LeafNode
import re 

def extract_markdown_images(text):
    """
    Docstring for extract_markdown_images
    
    :param text: Text to look for images in
    
    "return: List of tuples with image's alt text and url [(alt,  url), ...]

    Uses regular expressions to find images in markdown formatted strings.
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    """
    Docstring for extract_markdown_links
    
    :param text: Text to look for links in
    
    "return: List of tuples with link's text and url [(text,  url), ...]

    Uses regular expressions to find links in markdown formatted strings.
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Docstring for split_nodes_delimiter
    
    :param old_nodes: List of textnode objects to be processed
    :param delimiter: Delimiter character to split on
    :param text_type: Text type of node assigned to characters within delimiters

    If an old_node is not of type TextType.Text, then the old_node is left unchanged.

    :return: List of converted nodes 
    """
    converted_nodes = []
    for node in old_nodes:
        # 1. Only convert text nodes
        if node.text_type != TextType.TEXT:
            converted_nodes.append(node)
            continue
        split_node_text = node.text.split(delimiter)
        # 2. No delimiter found nothing to convert
        if len(split_node_text) == 1:
            converted_nodes.append(node)
            continue
        # 3. No matching closing delimiter found, can't convert, raise Error
        if len(split_node_text) % 2 == 0:
            raise Exception("Invalid markdown,  formatted section not closed")
        # 4. Take split text and place into nodes of corresponding type
        split_nodes = []
        for i in range(len(split_node_text)):
            # Don't create empty text nodes
            if split_node_text[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append( TextNode(split_node_text[i], TextType.TEXT) )
            else:
                split_nodes.append( TextNode(split_node_text[i], text_type) )
        # 5. Append new nodes to list of converted nodes
        converted_nodes.extend(split_nodes)
    # 6. Return all converted nodes
    return converted_nodes


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid text_type property")


def _split_nodes_by_pattern(old_nodes, extract_fn, markdown_fmt, new_type):
    converted_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            converted_nodes.append(node)
            continue
        
        matches = extract_fn(node.text)
        if len(matches) == 0:
            converted_nodes.append(node)
            continue
        
        text = node.text
        for label, url in matches:
            pattern = markdown_fmt.format(label=label, url=url)
            pre, text = text.split(pattern, 1)
            if pre != "":
                converted_nodes.append(TextNode(pre, TextType.TEXT))
            converted_nodes.append(TextNode(label, new_type, url))
        
        if text != "":
            converted_nodes.append(TextNode(text, TextType.TEXT))
    return converted_nodes


def split_nodes_image(old_nodes):
    return _split_nodes_by_pattern( 
        old_nodes, 
        extract_markdown_images, 
        "![{label}]({url})", 
        TextType.IMAGE,
    )


def split_nodes_link(old_nodes):
    return _split_nodes_by_pattern(
        old_nodes,
        extract_markdown_links,
        "[{label}]({url})",
        TextType.LINK,
    )


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    # Handle Images and Links 
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # Handle inline formatting
    delimiters = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    ]
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    return nodes