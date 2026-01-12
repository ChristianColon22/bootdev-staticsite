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
