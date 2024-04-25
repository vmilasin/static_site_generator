from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_delimiter
from textnode import TextNode



def main():
    node = TextNode("bold, This is text with a **bolded** word *and **bold** italic* `code text` text", "text")
    split_nodes_delimiter([node], "**", "bold")


    #node = TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png), AND HERE'S SOME MORE TEXT ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", "text")
    #split_nodes_image([node])

main()