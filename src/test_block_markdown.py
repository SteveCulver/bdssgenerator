import unittest

from src.block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_empty(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ],
        )        
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_multiple_blank_lines(self):
        md = """
This is the first block.


This is the second block.



This is the third block.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is the first block.",
                "This is the second block.",
                "This is the third block.",
            ],
        )

    def test_markdown_to_blocks_single_block_markdown(self):
        md = """
# Just one block here
This is a simple paragraph without any blank lines separating it from other content.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Just one block here\nThis is a simple paragraph without any blank lines separating it from other content."
            ]
        )
    
    def test_markdown_to_blocks_leading_or_trailing_whitespace(self):
        md = """  
   # Heading with leading spaces

This is a paragraph with  trailing spaces.   
  Another line in the same paragraph.

- List item 1
 - List item 2
   - List item 3  
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with leading spaces",
                "This is a paragraph with  trailing spaces.   \n  Another line in the same paragraph.",
                "- List item 1\n - List item 2\n   - List item 3"
            ]
        )

    def test_block_to_blocktype_heading_one(self):
        md = "# Heading"
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_two(self):
        md = "## Heading"
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_three(self):
        md = "### Heading"
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.HEADING,
        )               

    def test_block_to_blocktype_heading_four(self):
        md = "#### Heading"
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_five(self):
        md = "##### Heading"
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_six(self):
        md = "###### Heading"
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_seven(self):
        md = "####### Heading"
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_blocktype_heading_no_space(self):
        md = "#Heading"
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_blocktype_heading_space_but_no_header(self):
        md = "# "
        returned_type = block_to_block_type(md)
        self.assertEqual(
            returned_type,
            BlockType.PARAGRAPH,
        )
    
    # code type
    def test_block_type_code_simple(self):
        block = "```\nprint('hi')\n```"
        assert block_to_block_type(block) == BlockType.CODE       

    # TODO: Should probably add this check?
    def test_block_type_code_with_language(self):
        block = "```python\nx = 1\n```"
        assert block_to_block_type(block) == BlockType.CODE

    def test_block_type_code_two_lines(self):
        block = "```\n```"
        returned_type = block_to_block_type(block)
        assert returned_type == BlockType.CODE
     
    def test_block_type_code_missing_closing_fence(self):
        block = "```\nprint('hi')"
        assert block_to_block_type(block) == BlockType.PARAGRAPH


    # quote block
    def test_quote_block_valid(self):
        block = "> line one\n> line two"
        assert block_to_block_type(block) == BlockType.QUOTE

    def test_quote_block_invalid_missing_marker(self):
        block = "> line one\nline two"
        assert block_to_block_type(block) != BlockType.QUOTE

    # unordered list
    def test_unordered_list_valid(self):
        block = "- item one\n- item two"
        assert block_to_block_type(block) == BlockType.UNORDERED_LIST

    def test_unordered_list_invalid_no_space(self):
        block = "-item one\n- item two"
        assert block_to_block_type(block) != BlockType.UNORDERED_LIST

    # ordered list
    def test_ordered_list_valid_incrementing(self):
        block = "1. first\n2. second\n3. third"
        assert block_to_block_type(block) == BlockType.ORDERED_LIST

    def test_ordered_list_invalid_skips_number(self):
        block = "1. first\n3. third"
        assert block_to_block_type(block) != BlockType.ORDERED_LIST

    # Corner cases
    def test_empty_block(self):
        block = ""
        with self.assertRaises(ValueError) as e:
            block_to_block_type(block)

        self.assertEqual(str(e.exception), "markdown block is None or a blank string")

    def test_none_block(self):
        block = None
        with self.assertRaises(ValueError) as e:
            block_to_block_type(block)

        self.assertEqual(str(e.exception), "markdown block is None or a blank string")

    def test_paragraph(self):
        md = """
This is a simple paragraph with `code` and **bold**.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a simple paragraph with <code>code</code> and <b>bold</b>.</p></div>",
        )

    def test_heading_h1(self):
        md = """
# Big Title
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Big Title</h1></div>")

    def test_heading_h3_inline(self):
        md = """
### Mid Title with _italics_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>Mid Title with <i>italics</i></h3></div>")

    def test_code_block(self):
        md = """
```
This _is_ **raw** code
line2
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This _is_ **raw** code\nline2\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
> A wise quote
> with `code` and **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>A wise quote\nwith <code>code</code> and <b>bold</b></blockquote></div>",
        )

# python
    def test_unordered_list(self):
        md = """
- one item
- two `code`
- three **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one item</li>\n<li>two <code>code</code></li>\n<li>three <b>bold</b></li>\n</ul></div>",
        )

# python
    def test_ordered_list(self):
        md = """
1. first
2. second _italic_
3. third **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li>\n<li>second <i>italic</i></li>\n<li>third <b>bold</b></li>\n</ol></div>",
        )