import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_instance_creation(self):
        props_for_html_dummy = {"href": "https://www.google.com", "target": "_blank"}
        dummy_html_node = HTMLNode("a", "this is a link", None, props=props_for_html_dummy)
        self.assertIsInstance(dummy_html_node, HTMLNode)

    def test_single_prop(self):
        props_for_html_dummy = {"href": "https://www.google.com"}
        expected_html = ' href="https://www.google.com"'
        dummy_html_node = HTMLNode("a", "this is a link", None, props=props_for_html_dummy)
        self.assertEqual(dummy_html_node.props_to_html(), expected_html)

    def test_multi_prop(self):
        props_for_html_dummy = {"href": "https://www.google.com", "target": "__blank"}
        expected_html = ' href="https://www.google.com" target="__blank"'
        dummy_html_node = HTMLNode("a", "this is a link", None, props=props_for_html_dummy)
        self.assertEqual(dummy_html_node.props_to_html(), expected_html)


class TestLeafNode(unittest.TestCase):
    def test_instance_creation_no_prop(self):
        dummy_leaf_node = LeafNode("p", "this is just a paragraph", None)
        self.assertIsInstance(dummy_leaf_node, LeafNode)

    def test_instance_creation_prop(self):
        props_for_leaf_dummy = {"href": "https://www.google.com", "target": "__blank"}
        dummy_leaf_node = LeafNode("a", "this is a link", props_for_leaf_dummy)
        self.assertIsInstance(dummy_leaf_node, LeafNode)

    def test_instance_no_tag(self):
        dummy_leaf_node = LeafNode(None, "this should be returned as raw", None)
        self.assertIsInstance(dummy_leaf_node, LeafNode)
    
    def test_to_html_no_val(self):
        with self.assertRaises(TypeError):
            dummy_leaf_node = LeafNode("p", None, None)

    def test_to_html_no_tag(self):
        dummy_leaf_node = LeafNode(None, "this should be returned as raw", None)
        self.assertEqual(dummy_leaf_node.to_html(), dummy_leaf_node.value)

    def test_to_html_no_tag_with_props(self):
        props_for_leaf_dummy = {"href": "https://www.google.com", "target": "__blank"}
        dummy_leaf_node = LeafNode(None, "this should be returned as raw", props_for_leaf_dummy)
        self.assertEqual(dummy_leaf_node.to_html(), dummy_leaf_node.value)

    def test_to_html_with_tag_with_prop(self):
        props_for_leaf_dummy = {"href": "https://www.google.com", "target": "__blank"}
        dummy_leaf_node = LeafNode("a", "this is a link", props_for_leaf_dummy)
        expected_html = '<a href="https://www.google.com" target="__blank">this is a link</a>'
        self.assertEqual(dummy_leaf_node.to_html(), expected_html)

    def test_to_html_with_tag_no_prop(self):
        dummy_leaf_node = LeafNode("p", "this is just a paragraph", None)
        expected_html = '<p>this is just a paragraph</p>'
        self.assertEqual(dummy_leaf_node.to_html(), expected_html)


class TestParentNode(unittest.TestCase):
    x = LeafNode("b", "Bold text", None)
    y = LeafNode(None, "Normal text", None)
    z = LeafNode("i", "Italic text", None)
    m = LeafNode(None, "Normal text", None)
    n = LeafNode("a", "Hyperlink", {"href": "https://www.google.com", "target": "__blank"})

    parent_no_props = ParentNode("p", [x, y, z, m, n], None)
    parent_with_props = ParentNode("a", [x, y, z, m, n], {"href": "https://www.google.com", "target": "__blank"})
    nested_parent = ParentNode("a", [x, y, parent_no_props, n])

    def test_instance_parent_props(self):
        self.assertIsInstance(self.parent_with_props, ParentNode)
    
    def test_instance_parent_no_props(self):
        self.assertIsInstance(self.parent_no_props, ParentNode)

    def test_instance_parent_no_tag(self):
        with self.assertRaises(ValueError):
            parent_with_no_tag = ParentNode(None, [self.x, self.y, self.n], None)
            parent_with_no_tag.to_html()

    def test_instance_parent_no_children(self):
        with self.assertRaises(ValueError):
            parent_with_no_children = ParentNode("p", None, None)
            parent_with_no_children.to_html()

    def test_instance_parent_children_contains_parent(self):
        self.assertIsInstance(self.nested_parent, ParentNode)