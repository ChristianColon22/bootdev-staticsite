from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag is "":
            raise ValueError("parent nodes must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("parent nodes must have children")
        properties = ""
        if self.props is not None and len(self.props) != 0:
            properties = self.props_to_html()
        s = f"<{self.tag}{properties}>"
        for child in self.children:
            s += child.to_html()
        s += f"</{self.tag}>"
        return s
