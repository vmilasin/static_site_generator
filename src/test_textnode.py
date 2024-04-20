import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_attributes_text(self):
        with self.assertRaises(TypeError):
            node1 = TextNode(None, "bold", "https://www.google.com")

    def test_attributes_text_integer(self):
        with self.assertRaises(TypeError):
            node1 = TextNode(12345, "bold", "https://www.google.com")

    def test_attributes_text_type(self):
        with self.assertRaises(TypeError):
            node1 = TextNode("This is a text node", None, "https://www.google.com")

    def test_attributes_url(self):
        with self.assertRaises(TypeError):
            node1 = TextNode("This is a text node", "bold", None)

    def test_eq(self):
        node1 = TextNode("This is a text node", "bold", "https://www.google.com")
        node2 = TextNode("This is a text node", "bold", "https://www.google.com")
        self.assertEqual(node1, node2)

    



if __name__ == "__main__":
    unittest.main()