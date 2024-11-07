class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented in base class")

    def props_to_html(self):
        if not self.props:
            return ""
        html = ""
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children={self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("HTML leaf node must contain a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("HTML parent node must contain a tag")
        if not self.children or len(self.children) == 0:
            raise ValueError("HTML parent node must contain children nodes")
        
        child_html = ""
        for child in self.children:
            if child:
                child_html += child.to_html()
        return f"<{self.tag}{super().props_to_html()}>{child_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children={self.children}, {self.props})"