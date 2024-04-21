from inline_markdown import extract_markdown_images, extract_markdown_links



def main():
    text1 = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    text2 = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

    print(extract_markdown_images(text1))
    print(extract_markdown_links(text2))


main()