import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode


class TestInlineMarkdown(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", "text")
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word", "text"),
            ],
            new_nodes
        )

    def test_delimiter_bold__alternate(self):
        node = TextNode("This is text with a __bolded__ word", "text")
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word", "text"),
            ],
            new_nodes
        )

    def test_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word", "text")
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word", "text"),
            ],
            new_nodes
        )

    def test_delimiter_italic_alternate(self):
        node = TextNode("This is text with a _italic_ word", "text")
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word", "text"),
            ],
            new_nodes
        )

    def test_delimiter_striketrough(self):
        node = TextNode("This is text with a ~~striketrough~~ word", "text")
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("striketrough", "striketrough"),
                TextNode(" word", "text"),
            ],
            new_nodes
        )

    def test_delimiter_code(self):
        node = TextNode("This is text with a `code` word", "text")
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("code", "code"),
                TextNode(" word", "text"),
            ],
            new_nodes
        )

    def test_delimiter_bold_multi(self):
        node = TextNode("This is text with a **bolded** word **and another** word", "text")
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word ", "text"),
                TextNode("and another", "bold"),
                TextNode(" word", "text"),
            ],
            new_nodes
        )
    
    def test_delimiter_bold_multi_special_ending(self):
        node = TextNode("This is text with a **bolded** word **and another**", "text")
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word ", "text"),
                TextNode("and another", "bold"),
            ],
            new_nodes
        )
    