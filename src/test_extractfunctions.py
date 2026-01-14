import unittest
from extractfunctions import extract_markdown_images, extract_markdown_links

class TestExtractFunctions(unittest.TestCase):
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