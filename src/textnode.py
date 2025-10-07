from enum import Enum

class TextType(Enum):
    TEXT="text"
    BOLD="bold"
    ITALIC="italic"
    CODE="code"
    LINK="link"
    IMAGE="image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    # TODO: Need to add tests for this
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    from src.leafnode import LeafNode
    from src.textnode import TextNode, TextType  # safe import; already loaded

    # Check to see that text_node is actually of type textnode
    if not isinstance(text_node, TextNode):
        raise TypeError("text_node must be a TextNode")

    # optional: validate required fields
    if text_node.text_type == TextType.LINK and not text_node.url:
        raise ValueError("LINK requires a url")
    if text_node.text_type == TextType.IMAGE and (not text_node.url or text_node.text is None):
        raise ValueError("IMAGE requires url (src) and text (alt)")

    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src":text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
  
