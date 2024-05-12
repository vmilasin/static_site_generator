import os, shutil

def copy_directory_content(src_directory, dest_directory):
    # Check if the source directory is missing - if yes, create it
    if not os.path.exists(dest_directory):
        os.mkdir(dest_directory)
    
    # Check if the source directory is missing
    if os.path.exists(src_directory):
        # List the files in the source directory
        dir_list = os.listdir(src_directory)

        # Create file paths and copy files
        for file in dir_list:
            src_path = os.path.join(src_directory, file)
            dest_path = os.path.join(dest_directory, file)

            # If the source path is a folder, run the function recursively for all files in that folder
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
            else:
                copy_directory_content(src_path, dest_path)
    
    # Raise an error if the source directory is missing
    else:
        raise Exception("Source directory for content copy missing")