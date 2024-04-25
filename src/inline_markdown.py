import re

from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        # If the node is a text node, just append it as-is
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        
        split_nodes = []
        children = node.text.split(delimiter)
        
        # Raise a ValueError if there's a missing delimiter
        if len(children) % 2 == 0:
            raise ValueError(f"Invalid markdown, formatted {delimiter} section not closed")
        
        for i in range(len(children)):
            # Skip nodes begining with a delimiter
            if children[i] == "":
                continue
            # The node is split so that the first index (0) is text,
            if i % 2 == 0:
                split_nodes.append(TextNode(children[i], "text"))
            # The second child node contains special formatting
            else:
                split_nodes.append(TextNode(children[i], text_type))

        new_nodes.extend(split_nodes)
    return new_nodes



def extract_markdown_images(text):
    '''
    Takes raw text and returns a list of tuples. 
    Each tuple should contain the alt text and the URL of any markdown images. 
    
    For example:
    text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    
    print(extract_markdown_images(text))
    # [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
    '''

    image_data = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return list(image_data)

def extract_markdown_links(text):
    '''
    This one should extract markdown links instead of images.
    It should return tuples of anchor text and URLs. 
    
    For example:
    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    
    print(extract_markdown_links(text))
    # [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
    '''

    link_data = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return list(link_data)



def split_nodes_image(old_nodes):
    new_nodes = []

    # Check if the child starts with an image (used later)
    image_at_slice_start = lambda text: True if text.startswith("![") else False    

    for node in old_nodes:
        node_type = node.text_type
        node_text = node.text
        extracted_images = extract_markdown_images(node_text)

        split_nodes = []
        
        if not extracted_images:
            split_nodes.append(node)
        else:
            # To avoid looping over the same node multiple times due to multiple indices, use slicing to skip formatted text
            # Create an index to be used in slicing
            starting_index = 0          
            for image in extracted_images:
                # Each image consists of 5 markup characters, its text and URL - calculate length to be used in slicing
                image_length = 5 + len(image[0]) + len(image[1])

                # Slice the node starting from the last known index to the image (te rest is discarded)
                children = node_text[starting_index:].split(f"![{image[0]}]({image[1]})", maxsplit=1)

                #If there is only 1 extracted image, append both parts at the same time, since there is only 1 iteration
                if len(extracted_images) == 1:
                    for child in children:
                        if child:
                            if image_at_slice_start(node_text[starting_index:]) == True:
                                split_nodes.append(TextNode(image[0], "image", image[1]))
                                starting_index += image_length
                                split_nodes.append(TextNode(child, node_type))
                                starting_index += len(child)
                            else:
                                split_nodes.append(TextNode(child, node_type))
                                starting_index += len(child)
                                split_nodes.append(TextNode(image[0], "image", image[1]))
                                starting_index += image_length
                else:
                    for child in children:
                        if child:
                            # If the slice starts with an image, add the image to new nodes and increase the starting index by image data length
                            if image_at_slice_start(node_text[starting_index:]) == True:
                                split_nodes.append(TextNode(image[0], "image", image[1]))
                                starting_index += image_length
                            # Otherwise, add the child data and increase the starting index by child data length
                            else:
                                split_nodes.append(TextNode(child, node_type))
                                starting_index += len(child)

            # Don't forget to slice the remaining text after the last split
            if starting_index != len(node_text):
                remainder = node_text[starting_index:]
                if image_at_slice_start(remainder):
                    split_nodes.append(TextNode(image[0], "image", image[1]))
                else:
                    split_nodes.append(TextNode(child, node_type))
            else:
                pass
        new_nodes.extend(split_nodes)   
    return new_nodes