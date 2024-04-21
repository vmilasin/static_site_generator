from textnode import TextNode
from inline_markdown import split_nodes_delimiter



def main():
    node1 = TextNode("This is text with a **bolded** word", "text")
    node2 = TextNode("This is text with a *italic* word", "text")
    node3 = TextNode("This is a text with no special syntax", "text")
    node4 = TextNode("This is text with a ~~striketrough~~ word", "text")

    split_nodes_delimiter([node1])
    print("#####################")
    split_nodes_delimiter([node2])
    print("#####################")
    split_nodes_delimiter([node1, node2])
    print("#####################")
    split_nodes_delimiter([node4])


main()