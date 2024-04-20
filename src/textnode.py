from htmlnode import LeafNode

class TextNode:
    '''
    TextNode is sort of an intermediate representation between Markdown and HTML, and is specific to inline markup.

    The constuctor for TextNode has 3 properties which are passed to the constructor:
    
    self.text - The text content of the node
    self.text_type - The type of text this node contains, which is just a string like "bold" or "italic"
    self.url - The URL of the link or image, if the text is a link. Default to None if nothing is passed in.

    '''
    def __init__(self, text, text_type, url):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        if not isinstance(text_type, str):
            raise TypeError("Text type must be a string")
        if not isinstance(url, str):
            raise TypeError("URL must be a string")
        
        self.text = text
        self.text_type = text_type
        self.url = url

    
    def __eq__(self, other):
        if (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        ):
            return True
        return False
    
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    


def text_node_to_html_node(text_node):
    # Create LeafNodes based on TextNode types

    # Check the type and store it in a variable, so that you don't have to call the function to check (and use memory) every time
    leaf_text_type = lambda text_type:{
        "text": None,
        "bold": "b",
        "italic" : "i",
        "code": "code",
        "striketrough": "striketrough",
        "link": "a",
        "image": "img"
    }.get(text_type, "Unknown")
    leaf_type = leaf_text_type(text_node.text_type)

    # Based on the type, create a LeafNode and return it
    if leaf_type == "Unknown":
        raise Exception("TextNode input is invalid")
    elif leaf_type == "a":
        new_html_node = LeafNode(leaf_type, text_node.text, {"href": text_node.url})
    elif leaf_type == "img":
        new_html_node = LeafNode(leaf_type, "", {"src": text_node.url, "alt": text_node.text})
    else:
        new_html_node = LeafNode(leaf_type, text_node.text)

    return new_html_node
