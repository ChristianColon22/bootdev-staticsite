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

