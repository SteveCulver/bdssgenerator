import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # When eq and url specified
    def test_eq_incl_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

    # When the url property is specified and not equal
    def test_ne_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.sandal.dev")
        self.assertNotEqual(node, node2)

    # When the url property is None
    def test_eq_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    # When text type property is different
    def test_ne_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    # When text is different
    def test_ne_text(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https:/www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, url="https://boot.dev")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Boot.dev")
        self.assertEqual(html.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("A bear", TextType.IMAGE, url="https://img/bear.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(html.props, {"src": "https://img/bear.png", "alt": "A bear"})

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node({"text": "x"})  # not a TextNode

    def test_unknown_text_type(self):
        class FakeType: pass
        bad = TextNode("x", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(bad)


if __name__ == "__main__":
    unittest.main()
