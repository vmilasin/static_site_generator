import os
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