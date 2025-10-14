import unittest

from block_markdown import markdown_to_blocks

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