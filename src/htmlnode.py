class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # string
        self.value = value # string 
        self.children = children # List of children
        self.props = props # Dictionary of properties

    def to_html(self):
        # Must be implemented by child classes
        raise NotImplementedError
    
    def props_to_html(self):
        s = ""
        if self.props is None:
            return s
        for k,v in self.props.items():
            s += f" {k}=\"{v}\""
        return s

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return str(self.value)
        properties = self.props_to_html() if self.props is not None else ""
        return f"<{self.tag}{properties}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
    
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

