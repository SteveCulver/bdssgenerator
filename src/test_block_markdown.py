import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
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
        print(returned_type)
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