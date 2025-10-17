from enum import Enum
import re
from src.htmlnode import HTMLNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node, TextNode
from src.parentnode import ParentNode
from src.leafnode import LeafNode
import inspect


def text_to_children(text):
    if not isinstance(text, str):
        raise TypeError(f"text_to_children expected str, got {type(text)}: {text}")
    
    # 1) parse inline markdown into TextNodes
    textnodes = text_to_textnodes(text)
    
    # 2) convert each TextNode into an HTMLNode
    children = []
    for tn in textnodes:
        #print("DEBUG tn type:", type(tn))  # <-- add
        #print("DEBUG TextNode id:", id(TextNode), "module:", inspect.getmodule(TextNode))
        #print("DEBUG tn class id:", id(tn.__class__), "module:", inspect.getmodule(tn.__class__))
        if not isinstance(tn, TextNode):
            raise TypeError(f"Expected TextNode, got {type(tn)}")       
        child = text_node_to_html_node(tn)
        children.append(child)
    # 3) return the list [HTMLNode]
    return children

# Converts a full markdown document into a single parent HTMLNode
# The one parent HTMLNode should contain many child HTMLNode objects representing
# the nested elements.
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # CODE
        if block_type == BlockType.CODE:
            lines = block.splitlines()
            inner = "\n".join(lines[1:-1]) + "\n"
            codeleaf = LeafNode(tag="code", value=inner)
            node = ParentNode(tag="pre", children=[codeleaf])
            children.append(node)
        # ORDERED
        if block_type == BlockType.ORDERED_LIST:
            rawlines = block.splitlines()
            li_nodes = []
            for line in rawlines:
                s = line.lstrip()
                if ". " in s:
                    num, rest = s.split(". ", 1)
                    if num.isdigit():
                        s = rest
                else:
                    s = line
                if not s:
                    continue
                li = ParentNode("li", children=text_to_children(s))
                li_nodes.append(li)
                li_nodes.append(LeafNode(tag=None,value="\n"))
            node = ParentNode(tag="ol", children=li_nodes)
            children.append(node)            
        # UNORDERED
        if block_type == BlockType.UNORDERED_LIST:
            rawlines = block.splitlines()
            li_nodes = []
            for line in rawlines:
                if line.startswith("-"):
                    line = line[1:]
                    if line.startswith(" "):
                        line = line[1:]
                if not line:
                    continue
                li = ParentNode("li", children=text_to_children(line))
                li_nodes.append(li)
                li_nodes.append(LeafNode(tag=None,value="\n"))
            node = ParentNode(tag="ul", children=li_nodes)
            children.append(node)
        # QUOTE
        if block_type == BlockType.QUOTE:
            rawlines = block.splitlines()
            cleaned = []
            for line in rawlines:
                if line.startswith(">"):
                    line = line[1:]
                    if line.startswith(" "):
                        line = line[1:]
                cleaned.append(line)
            inner = "\n".join(cleaned)
            node = ParentNode(tag="blockquote", children=text_to_children(inner))
            children.append(node)
        # HEADING
        elif block_type == BlockType.HEADING:
            leading_pounds = 0
            for c in block:
                if c == "#":
                    leading_pounds += 1
                else:
                    break
            level = min(leading_pounds, 6)
            text = block[leading_pounds:]
            if text.startswith(" "): text = text[1:]
            tag = f"h{level}"
            node = ParentNode(tag=tag, children=text_to_children(text))
            children.append(node)
        # PARAGRAPH
        elif block_type == BlockType.PARAGRAPH:
            node = ParentNode(tag="p",
                            children=text_to_children(block))
            children.append(node)

    parent = ParentNode(tag="div", children=children)
    return parent
    

# Block markdown is just the separation of different sections of an entire document
# In well-written markdown, blocks are separated by a single blank line
def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    new_blocks = []
    for block in blocks:
        b = block.strip()
        if len(b) == 0:
            continue
        new_blocks.append(b)
    return new_blocks

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"

def block_to_block_type(markdown_block):
    
    if markdown_block is None or markdown_block == "":
        raise ValueError("markdown block is None or a blank string")

    lines = markdown_block.splitlines()

    # Check for headings
    headings = re.findall(r"^(#{1,6})\s[\S]+", lines[0])

    if len(headings) > 0:
        return BlockType.HEADING
    
    if len(lines) >= 2:
        if lines[0].startswith("```") and lines[-1] == "```":
            return BlockType.CODE
    
    is_quote = True
    is_unordered = True
    is_ordered = True
    expected = 1

    for line in lines:
        is_quote &= line.startswith(">")
        is_unordered &= line.startswith("- ")
        if is_ordered:
            if line.startswith(f"{expected}. "):
                expected += 1
            else:
                is_ordered = False

    if is_quote:
        return BlockType.QUOTE
    elif is_unordered:
        return BlockType.UNORDERED_LIST
    elif is_ordered:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
