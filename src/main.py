from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_delimiter, split_nodes_link, text_to_textnodes
from textnode import TextNode



def main():
    node = TextNode("[link](https://www.google.com) This is text with a link [link](https://www.google.com)[different](https://www.bing.com) and [lizardman_boss](https://www.facebook.com)", "text")
    node2 = TextNode("[link](https://www.bing.com) This is text with a link [link](https://www.facebook.com) AND SOME MORE TEXT", "text")
    split_nodes_link([node])


    #node = TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png), AND HERE'S SOME MORE TEXT ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", "text")
    #split_nodes_image([node])

main()