
import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    # Multiple children
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span><span>child3</span></div>")

    # No children - empty list
    def test_to_html_with_no_children_empty(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    # No children - None
    def test_to_html_with_no_children_none(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        self.assertEqual(str(e.exception), "All parent nodes must have children")        

    # Parent nodes must have a tag
    def test_to_html_with_no_parent_node_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )

        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception), "All parent nodes must have a tag")

    # Nesting parentnode objects inside of one another
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # Test repr, and all options
    # no children, no props
    # ParentNode, no children
    def test_repr_exact_no_children_props_empty_dict(self):
        node = ParentNode(tag="div", children=[], props={})
        expected = "ParentNode(tag='div', children=[], props={})"
        self.assertEqual(repr(node), expected)

    def test_repr_exact_no_children_props_none(self):
        node = ParentNode(tag="div", children=[], props=None)
        expected = "ParentNode(tag='div', children=[], props=None)"
        self.assertEqual(repr(node), expected)

    def test_repr_exact_no_children_props_not_provided(self):
        node = ParentNode(tag="div", children=[])
        expected = "ParentNode(tag='div', children=[], props=None)"
        self.assertEqual(repr(node), expected)                   

    def test_repr_exact_no_children_props_specified(self):
        node = ParentNode(tag="div", children=[], props={"href": "x"})
        expected = "ParentNode(tag='div', children=[], props={'href': 'x'})"
        self.assertEqual(repr(node), expected)

    def test_repr_exact_nested_parents(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = "ParentNode(tag='div', children=[ParentNode(tag='span', children=[LeafNode(tag='b', value='grandchild', props=None)], props=None)], props=None)"
        self.assertEqual(repr(parent_node), expected)        

    def test_repr_exact_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        expected = "ParentNode(tag='div', children=[LeafNode(tag='span', value='child1', props=None), LeafNode(tag='span', value='child2', props=None)], props=None)"
        self.assertEqual(repr(parent_node), expected)


    #Test all the edge cases you can think of, including nesting ParentNode objects inside of one another, multiple children, and no children.
    def test_to_html_with_og_testcase(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
