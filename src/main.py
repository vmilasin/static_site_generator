import os, shutil
from copy_static import copy_directory_content
from generate_page import generate_pages_recursive

    
dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    # Delete contents of the public folder
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    # Copy contents from the static to public directory
    print("Copying static files to public directory...")
    copy_directory_content(dir_path_static, dir_path_public)

    # Generate a page from markdown
    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()