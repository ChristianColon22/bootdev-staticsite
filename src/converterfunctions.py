from textnode import TextNode, TextType
from leafnode import LeafNode
from extractfunctions import extract_markdown_images, extract_markdown_links 

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
