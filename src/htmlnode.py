import functools

class HTMLNode:
    '''
    The HTMLNode class will represent a "node" in an HTML document tree (like a <p> tag and its contents, or an <a> tag and its contents) and is purpose-built to render itself as HTML.

    The HTMLNode class should have 4 data members set in the constructor:

    tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    children - A list of HTMLNode objects representing the children of this node
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    Perhaps counterintuitively, every data member should be optional and default to None:

    An HTMLNode without a tag will just render as raw text
    An HTMLNode without a value will be assumed to have children
    An HTMLNode without children will be assumed to have a value
    An HTMLNode without props simply won't have any attributes

    '''
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props    
    
    
    def to_html(self):
        raise NotImplemented  


    def props_to_html(self):
        '''
        This method should return a string that represents the HTML attributes of the node.

        If self.props is:
        {"href": "https://www.google.com", "target": "_blank"}

        Then self.props_to_html() should return:
        href="https://www.google.com" target="_blank"

        '''
        
        if self.props == None:
            return ""
        else:
            html_attrs = []
            # Initialize with space after HTML tag
            html_attrs.append("")

            for prop, value in self.props.items():
                html_attrs.append(f'{prop}="{value}"')
            
            return ' '.join(html_attrs)
        
    
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"
    




class LeafNode(HTMLNode):
    '''
    A LeafNode is a type of HTMLNode that represents a single HTML tag with no children.

    For example, a simple <p> tag with some text inside of it:
    <p>This is a paragraph of text.</p>

    LeafNode constructor should differ slightly from the HTMLNode class because it shouldn't allow for children.
    The value data member should be required.
    '''
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        
        if value == None:
            raise TypeError("LeafNode value missing")
        
    def __repr__(self):
        return f"LeafNode(tag:{self.tag}, value:{self.value}, props:{self.props})"    
    

    def to_html(self):
        '''
        This method should render a leaf node as an HTML string (by returning a string).
        All leaf nodes require a value, if they do not, it should raise a ValueError.        
        If there is no tag (e.g. it's None), the value should be returned as raw text.

        Otherwise, it should render an HTML tag. For example, these leaf nodes:

        LeafNode("p", "This is a paragraph of text.")
        LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        Should render as:

        <p>This is a paragraph of text.</p>
        <a href="https://www.google.com">Click me!</a>
        '''            
        if self.tag == None:
            return self.value
        elif self.tag != None and self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    
        
class ParentNode(HTMLNode):
    '''
    This is the one that will handle the nesting of HTML nodes inside of one another.
    Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.
    Its constructor should differ from the parent class in that it doesn't take a value argument, and the children argument is not optional.
    '''
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def __repr__(self):
        return f"ParentNode(tag:{self.tag}, children:{self.children}, props:{self.props})"
        
    def to_html(self):
        '''
        If the tag is not provided, raise a ValueError.
        If there are no children, raise a ValueError with a different message.
        Otherwise, it should return a string representing the HTML tag of the node and its children.
        '''
        
        if self.tag == None:
            raise ValueError("ParentNode tag missing")
        elif self.children == None:
            raise ValueError("ParentNode children missing")
        else:
            get_leaf_node = lambda child: child.to_html()
            def get_leaf_nodes(result, node):
                return result + get_leaf_node(node)
            concat_leaf_nodes = functools.reduce(get_leaf_nodes, self.children, "")

            return f"<{self.tag}{self.props_to_html()}>{concat_leaf_nodes}</{self.tag}>"
            

