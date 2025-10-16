from enum import Enum
import re

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
    
    if markdown_block is None or markdown_block is "":
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
