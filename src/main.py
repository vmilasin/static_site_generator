import os, shutil
from copy_static import copy_directory_content   
    
dir_path_static = "./static"
dir_path_public = "./public"

def main():
    # Delete contents of the public folder and copy the contents from the static to public directory
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_directory_content(dir_path_static, dir_path_public)


main()