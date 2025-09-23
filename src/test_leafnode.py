import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):    
    # Positive case - tag and value present
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Leaf no value
    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception), "All leaf nodes must have a value")

    # tag ""
    def test_leaf_no_tag(self):
        node = LeafNode("", "Hello world!")
        self.assertEqual(node.to_html(), "Hello world!")

    # tag None
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(node.to_html(), "Hello world!")

    # tag with props
    def test_leaf_tag_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')