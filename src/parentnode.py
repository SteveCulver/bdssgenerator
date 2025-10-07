
from src.htmlnode import HTMLNode

# Handles the nesting of HTML nodes inside of one another.
# Any node that is not a leaf node (e.g. it has children) is a parent node

class ParentNode(HTMLNode):
    # tag and children arguments aren't optional
    # it doesn't take a value argument
    # props is optional
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, value=None, children=children, props=props)


    #node = ParentNode(
    #    "p",
    #    [
    #        LeafNode("b", "Bold text"),
    #        LeafNode(None, "Normal text"),
    #        LeafNode("i", "italic text"),
    #        LeafNode(None, "Normal text"),
    #    ],
    #)
    #
    #node.to_html()

    # should convert to 
    # <p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None or self.children is []:
            raise ValueError("All parent nodes must have children")
        else:            
            child_results = ""
            for c in self.children:
                child_results += c.to_html()
            
            return f"<{self.tag}{self.props_to_html()}>{child_results}</{self.tag}>"
        
    def __repr__(self):
        return (f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})")
