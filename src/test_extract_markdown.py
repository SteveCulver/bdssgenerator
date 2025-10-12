import unittest

from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links
)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images(
            "This is text with no image)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_image_link_and_markdown_link(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif")], matches)

    def test_extract_markdown_images_only_markdown_link(self):
        matches = extract_markdown_images(
            "This is text with a markdown link [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links(
            "This is text with a link but there isn't a link"
        )
        self.assertListEqual([], matches)    

    def test_extract_markdown_links_image_link_and_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links_only_image_link(self):
        matches = extract_markdown_links(
            "This is text with a markdown link ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([], matches)            

if __name__ == "__main__":
    unittest.main()