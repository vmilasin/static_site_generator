import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode


class TestInlineMarkdownDelimiter(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
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
        new_nodes = split_nodes_delimiter([node], "__", "bold")
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
        new_nodes = split_nodes_delimiter([node], "*", "italic")
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
        new_nodes = split_nodes_delimiter([node], "_", "italic")
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
        new_nodes = split_nodes_delimiter([node], "~~", "striketrough")
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
        new_nodes = split_nodes_delimiter([node], "`", "code")
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
        new_nodes = split_nodes_delimiter([node], "**", "bold")
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
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word ", "text"),
                TextNode("and another", "bold"),
            ],
            new_nodes
        )


    
class TestInnlineMarkdownImageExtraction(unittest.TestCase):
    def test_extract_markdown_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        desired_result = [('image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'), ('another', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png')]
        self.assertListEqual(extract_markdown_images(text), desired_result)


class TestInlineMarkdownLinkExtraction(unittest.TestCase):
    def test_extract_markdown_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        desired_result = [('link', 'https://www.example.com'), ('another', 'https://www.example.com/another')]
        self.assertListEqual(extract_markdown_links(text), desired_result)


class TestInlineMarkdownImageSplit(unittest.TestCase):
    def test_split_image_one_trailing(self):
        node = TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", "text")
        desired_result = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertListEqual(split_nodes_image([node]), desired_result)

    def test_split_image_one_leading(self):
        node = TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) This is text with an image", "text")
        desired_result = [            
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" This is text with an image", "text"),
        ]
        self.assertListEqual(split_nodes_image([node]), desired_result)

    def test_split_image_multiple_end_with_image(self):
        node = TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) This is text with an image ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", "text")
        desired_result = [            
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" This is text with an image ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertListEqual(split_nodes_image([node]), desired_result)

    def test_split_image_multiple_end_with_text(self):
        node = TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) This is text with an image ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) AND SOME MORE TEXT", "text")
        desired_result = [            
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" This is text with an image ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" AND SOME MORE TEXT", "text"),
        ]
        self.assertListEqual(split_nodes_image([node]), desired_result)

    def test_split_image_multiple_concurrent_images(self):
        self.maxDiff = None
        node = TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png), AND HERE'S SOME MORE TEXT ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", "text")
        desired_result = [            
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ", "text"),
            TextNode("another", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(", AND HERE'S SOME MORE TEXT ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertListEqual(split_nodes_image([node]), desired_result)


class TestInlineMarkdownLinkSplit(unittest.TestCase):
    def test_split_link_one_trailing(self):
        node = TextNode("This is text with a [link](https://www.google.com)", "text")
        desired_result = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.google.com"),
        ]
        self.assertListEqual(split_nodes_link([node]), desired_result)

    def test_split_link_one_leading(self):
        node = TextNode("[link](https://www.google.com) This is text with a link", "text")
        desired_result = [            
            TextNode("link", "link", "https://www.google.com"),
            TextNode(" This is text with a link", "text"),
        ]
        self.assertListEqual(split_nodes_link([node]), desired_result)

    def test_split_link_multiple_end_with_link(self):
        node = TextNode("[link](https://www.google.com) This is text with a link [link](https://www.google.com)", "text")
        desired_result = [            
            TextNode("link", "link", "https://www.google.com"),
            TextNode(" This is text with a link ", "text"),
            TextNode("link", "link", "https://www.google.com"),
        ]
        self.assertListEqual(split_nodes_link([node]), desired_result)

    def test_split_link_multiple_end_with_text(self):
        node = TextNode("[link](https://www.google.com) This is text with a link [link](https://www.google.com) AND SOME MORE TEXT", "text")
        desired_result = [            
            TextNode("link", "link", "https://www.google.com"),
            TextNode(" This is text with a link ", "text"),
            TextNode("link", "link", "https://www.google.com"),
            TextNode(" AND SOME MORE TEXT", "text"),
        ]
        self.assertListEqual(split_nodes_link([node]), desired_result)

    def test_split_link_multiple_concurrent_links(self):
        self.maxDiff = None
        node = TextNode("[link](https://www.google.com) This is text with a link [link](https://www.google.com)[different](https://www.bing.com) and [lizardman_boss](https://www.facebook.com)", "text")
        desired_result = [            
            TextNode("link", "link", "https://www.google.com"),
            TextNode(" This is text with a link ", "text"),
            TextNode("link", "link", "https://www.google.com"),
            TextNode("different", "link", "https://www.bing.com"),
            TextNode(" and ", "text"),
            TextNode("lizardman_boss", "link", "https://www.facebook.com"),
        ]
        self.assertListEqual(split_nodes_link([node]), desired_result)



class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_image_only(self):
        node = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        desired_result = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertListEqual(text_to_textnodes(node), desired_result)

    def test_text_to_textnodes_link_only(self):
        node = "This is text with a [link](https://www.google.com)"
        desired_result = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.google.com"),
        ]
        self.assertListEqual(text_to_textnodes(node), desired_result)

    def test_text_to_textnodes_delimiter_only(self):
        node = "This is text with a **bolded** word *and another italic* word"
        desired_result= [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word ", "text"),
            TextNode("and another italic", "italic"),
            TextNode(" word", "text"),
        ]
        self.assertListEqual(text_to_textnodes(node), desired_result)

    def test_text_to_textnodes_all(self):
        self.maxDiff = None
        node = "This is text with an image ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png), a **bolded** word *and another italic* word, ending with a link [link](https://www.google.com)!"
        desired_result= [
            TextNode("This is text with an image ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(", a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word ", "text"),
            TextNode("and another italic", "italic"),
            TextNode(" word, ending with a link ", "text"),
            TextNode("link", "link", "https://www.google.com"),
            TextNode("!", "text"),
        ]
        self.assertListEqual(text_to_textnodes(node), desired_result)


if __name__ == "__main__":
    unittest.main()