import unittest

from src.htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html_ne(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError) as e:
            node.to_html()
        self.assertEqual(str(e.exception), "Child classes will override this method to render themselves as HTML")

    # Default returns ""
    def test_props_to_html_default_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    # Empty None returns ""
    def test_props_to_html_default_empty_dict(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    # Empty dict returns ""
    def test_props_to_html_default_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_dict_one_value(self):
        node = HTMLNode(props={"foo": "bar"})
        out = node.props_to_html()
        expectedOut = ' foo="bar"'
        self.assertEqual(expectedOut, out)

    # Multple props are returned in ascending key order
    def test_props_to_html_dict_multi_value(self):
        node = HTMLNode(props={"foo": "bar", "bar": "foo", "car": "shar"})
        out = node.props_to_html()
        expectedOut = ' bar="foo" car="shar" foo="bar"'
        self.assertEqual(expectedOut, out)
 
    # no children, no props
    def test_repr_exact_no_children_no_props(self):
        node = HTMLNode(tag="a", value="link", children=[], props={})
        expected = "HTMLNode(tag='a', value='link', children=[], props={})"
        self.assertEqual(repr(node), expected)        

    # no children, everything else defined
    def test_repr_exact_no_children(self):
        node = HTMLNode(tag="a", value="link", children=[], props={"href": "x"})
        expected = "HTMLNode(tag='a', value='link', children=[], props={'href': 'x'})"
        self.assertEqual(repr(node), expected)  

    # no props
    def test_repr_exact_no_props(self):
        node = HTMLNode(tag="a", value="link", children=[HTMLNode(value="child")], props={})
        expected = "HTMLNode(tag='a', value='link', children=[HTMLNode(tag=None, value='child', children=None, props=None)], props={})"
        self.assertEqual(repr(node), expected)      