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

    child_starts_with_image = lambda x: True if x.startswith("![") else False  

    for node in old_nodes:
        node_type = node.text_type
        node_text = node.text
        # Check node for images
        extracted_images = extract_markdown_images(node_text)
        
        # If there are no images in the node, append it as-is
        if not extracted_images:
            new_nodes.append(node)
        
        # Otherwise split the node on each image
        # When splitting the node, there will be 2 parts - one empty (the image currently being split) and one other
        else:
            # To avoid looping over the same node multiple times due to multiple indices, use slicing to skip formatted text
            # Create an index to be used in slicing
            starting_index = 0
            images_added = 0            

            for image in extracted_images:
                # Each image consists of 5 markup characters, its text and URL - calculate length to be used in slicing
                image_length = 5 + len(image[0]) + len(image[1])

                # The node text is going to be split on a new starting index after each iteration
                # If there is a image in the node, the starting index will be increased by the image length
                # If there is something other than a image in the node before the image, the index will be increased by that data length
                children = node_text[starting_index:].split(f"![{image[0]}]({image[1]})", maxsplit=1)

                for child in children:
                    if child:                        
                        # If there are same 2 concurrent images, just continue on a child that starts with the image markup
                        # Usually, when nodes start with an image, they return an empty string on splitting
                        # Otherwise you might split the node twice on the same image and that will break your slicing
                        if child_starts_with_image(child) and children[0] != "":
                            continue
                        
                        # If the child is an empty string - that is the result of an image being split from the node, add it to the result
                        # If the child starts with a non-empty string, append that part that comes before the image along with the image that follows it
                        if children[0] != "":
                            new_nodes.append(TextNode(child, node_type))
                            starting_index += len(child)
                        
                        # If the ammount of added images is the same as the ammount of extracted images, skip adding an image node to
                        # avoid duplication when the last node is a text node
                        if images_added == len(extracted_images):
                            continue
                        new_nodes.append(TextNode(image[0], "image", image[1]))
                        starting_index += image_length
                        images_added += 1                        

            # Since we are splitting on extracted images - if the remaining slice contains anything other than an empty string,
            # that means that there's additonal node content left over after the last split, so append it to the results as-is
            if node_text[starting_index:]:
                new_nodes.append(TextNode(node_text[starting_index:], node_type))
    return new_nodes




def split_nodes_link(old_nodes):
    new_nodes = []  

    child_starts_with_link = lambda x: True if x.startswith("[") else False

    for node in old_nodes:
        node_type = node.text_type
        node_text = node.text
        # Check node for links
        extracted_links = extract_markdown_links(node_text)

        # If there are no links in the node, append it as-is
        if not extracted_links:
            new_nodes.append(node)
        
        # Otherwise split the node on each link
        # When splitting the node, there will be 2 parts - one empty (the link currently being split) and one other
        else:
            # To avoid looping over the same node multiple times due to multiple indices, use slicing to skip formatted text
            # Create an index to be used in slicing
            starting_index = 0
            links_added = 0 

            for link in extracted_links:
                print(link)
                # Each link consists of 5 markup characters, its text and URL - calculate length to be used in slicing
                link_length = 4 + len(link[0]) + len(link[1])

                # The node text is going to be split on a new starting index after each iteration
                # If there is a link in the node, the starting index will be increased by the link length
                # If there is something other than a link in the node before the link, the index will be increased by that data length
                children = node_text[starting_index:].split(f"[{link[0]}]({link[1]})", maxsplit=1)

                for child in children:
                    print(children)
                    if child:
                        # If there are same 2 concurrent links, just continue on a child that starts with the link markup
                        # Usually, when nodes start with an link, they return an empty string on splitting
                        # Otherwise you might split the node twice on the same link and that will break your slicing                    
                        if child_starts_with_link(child):
                            continue
                        
                        # If the child is an empty string - that is the result of a link being split from the node, add it to the result
                        # If the child starts with a non-empty string, append that part that comes before the link along with the link that follows it
                        if children[0] != "":
                            new_nodes.append(TextNode(child, node_type))
                            starting_index += len(child)

                        # If the ammount of added images is the same as the ammount of extracted images, skip adding an image node to
                        # avoid duplication when the last node is a text node
                        if links_added == len(extracted_links):
                            continue
                        new_nodes.append(TextNode(link[0], "link", link[1]))
                        starting_index += link_length
                        links_added += 1 

            # Since we are splitting on extracted link - if the remaining slice contains anything other than an empty string,
            # that means that there's additonal node content left over after the last split, so append it to the results as-is
            if node_text[starting_index:]:
                new_nodes.append(TextNode(node_text[starting_index:], node_type))
    print(new_nodes)
    return new_nodes





def text_to_textnodes(text):
    # Check the delimiters, and get the defined type
    valid_delimiters = ["*", "_", "~", "`"]   
    textnode_type = lambda delimiter: {
        "" : "text",
        "**" : "bold",
        "__": "bold",
        "*" : "italic",
        "_" : "italic",
        "~~" : "striketrough",
        "`" : "code",
    }.get(delimiter, "Unknown")

    # Mechanism to check if a node contains any valid delimiters and return a sorted list by occurance in TextNode.text
    def check_nodes_for_delimiters(node):
        used_delimiters = []
        node_length = len(node.text)
        # For bold and italic text, check the next and previous indices, so that you dont add italic delimiters for bold text for example
        for i in range(0, node_length):
            char = node.text[i]
            previous_char = node.text[i-1]
            if i != node_length - 1:
                next_char = node.text[i+1]
            else:
                next_char = None

            # If the character is not in valid delimiter characters, skip
            if char not in valid_delimiters:
                continue
            # If the character is in in used delimiter list, skip (we iterate only once for each delimiter)
            elif char in used_delimiters:
                continue
            # Otherwise add to list of used delimiters (mind the double characters)
            # Doble character delimiter checks break operation - if special formatting is at the end of node
            # Since we don't need them (as we have already checked the opening delimiter - and they're unique), we can skip the check
            elif char in valid_delimiters and not (i == node_length - 1 or i == node_length -2):
                if (char == "*" and next_char == "*") and "**" not in used_delimiters:
                    used_delimiters.append("**")
                elif char == "*" and not (next_char == "*" or previous_char == "*"):
                    used_delimiters.append("*")
                elif char == "_" and next_char == "_" and "__" not in used_delimiters:
                    used_delimiters.append("__")
                elif char == "_" and not (next_char == "_" or previous_char == "_"):
                    used_delimiters.append("_") 
                elif char == "~" and next_char == "~" and "~~" not in used_delimiters:
                    used_delimiters.append("~~")               
                elif char == "`":
                    used_delimiters.append("`")
            else:
                continue
        if len(used_delimiters) == 0:
            return False        
        else:           
            return used_delimiters   
       
    
    results = split_nodes_image(text)
    results = split_nodes_link(results)

    # Get a list of all text delimiters
    for node in results:
        used_delimiters = check_nodes_for_delimiters(node)
        #print(used_delimiters)

        # We split only on nodes that contain delimiters
        if not used_delimiters:
            continue            
        else:        
            for delimiter in used_delimiters:
                results = split_nodes_delimiter(results, delimiter, textnode_type(delimiter))

    return results
        
