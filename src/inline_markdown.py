from textnode import TextNode


def split_nodes_delimiter(old_nodes):
    # If a TextNode contains different formatting (e.g.: italic text that is already bold), create child TextNode objects with their specific type defined

    # Check the delimiters, and get the defined type
    valid_delimiters = ["**", "__", "*", "_", "~~", "`"]    
    textnode_type = lambda delimiter: {
        "" : "text",
        "**" : "bold",
        "__": "bold",
        "*" : "italic",
        "_" : "italic",
        "~~" : "striketrough",
        "`" : "code",
        #"[title]" : "link",
        #"!" : "image"
    }.get(delimiter, "Unknown")

    new_nodes = []

    # Mechanism to check if a node contains any valid delimiters and return a sorted list by occurance in TextNode.text
    def check_nodes_for_delimiters(node):
        used_delimiters = []
        for valid_delimiter in valid_delimiters:
            if valid_delimiter in node.text:
                used_delimiters.append(valid_delimiter)

        if len(used_delimiters) == 0:
            return False
        
        else:
            used_delimiters = sorted(used_delimiters, key=lambda x: node.text.index(x))                
            return used_delimiters

    # Iterate over all TextNodes in old_nodes
    for node in old_nodes:
        node_text = node.text
        node_type = node.text_type
        used_delimiters = check_nodes_for_delimiters(node)

        if not used_delimiters:
            # If no delimiters were found in the node, just append it to new_nodes as-is
            new_nodes.append(node)
        
        else:
            # Otherwise, split the node and append its children
            for delimiter in used_delimiters:                
                if delimiter in node_text:
                    
                    # If the special formatting isn't closed, raise an error
                    if node_text.count(delimiter) % 2 != 0:
                        raise ValueError(f"Unmatched delimiter {delimiter} found")
                    
                    else:
                        children = node_text.split(delimiter)
                        # First part of text is of the default type
                        special_format = False
                            
                        for child in children:
                            # Check if the child segment contains text
                            if child:
                                # If the child is of the default type, just add it to new_nodes as-is
                                if not special_format:
                                    new_nodes.append(TextNode(child, node_type))
                                # Otherwise, add the child to new_nodes with its respective type
                                else:
                                    new_nodes.append(TextNode(child, textnode_type(delimiter)))
                                # We are either adding default type text, or we have come to the special type text that needs to be reformatted
                                # Either way, when we are done adding the previous child part, the next one type will be opposite than the previous part
                                special_format = not special_format

    return new_nodes