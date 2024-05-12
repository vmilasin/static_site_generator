import os
from pathlib import Path
from block_markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
        
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    markdown_file = open(from_path, "r")
    markdown_data = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path, "r")
    template_data = template_file.read()
    template_file.close()

    markdown_nodes = markdown_to_html_node(markdown_data)
    html_nodes = markdown_nodes.to_html()

    title = extract_title(markdown_data)
    template_data = template_data.replace("{{ Title }}", title)
    template_data = template_data.replace("{{ Content }}", html_nodes)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template_data)


def generate_pages_recursive(src_path_dir, template_path, dest_path_dir):    
    # Check if the source directory is missing
    if os.path.exists(src_path_dir):
        # List the files in the source directory
        dir_list = os.listdir(src_path_dir)

        # Create file paths and copy files
        for file in dir_list:
            src_path = os.path.join(src_path_dir, file)
            template_path = template_path
            dest_path = os.path.join(dest_path_dir, file)

            # If the source path is a folder, run the function recursively for all files in that folder
            if os.path.isfile(src_path):
                dest_path = Path(dest_path).with_suffix(".html")
                generate_page(src_path, template_path, dest_path)
            else:
                generate_pages_recursive(src_path, template_path, dest_path)
    
    # Raise an error if the source directory is missing
    else:
        raise Exception("Source directory for content copy missing")