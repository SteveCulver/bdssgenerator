from textnode import TextNode, TextType
import os
import shutil

# A recursive function that copies all contents from a source directory to a destination directory
def copy_all_contents(source_dir, destination_dir):
    source_dir = os.path.abspath(source_dir)
    destination_dir = os.path.abspath(destination_dir)

    # Delete all the contents of the destination directory, to ensure the copy is clean
    if not os.path.exists(source_dir):
        raise ValueError(f"source directory '{source_dir}' doesn't exist")
    
    if not os.path.exists(destination_dir):
        raise ValueError(f"destination directory '{destination_dir}' doesn't exist")
    
    print(f"Delete all the contents of destination: '{destination_dir}'")
    shutil.rmtree(path=destination_dir)
    os.mkdir(destination_dir)

    # Copy all files and subdirectories, nested files, etc.
    dir_contents = os.listdir(source_dir)
    print(f"processing dir: '{source_dir}', with contents: '{dir_contents}'")
    for content in dir_contents:
        content_path = os.path.join(source_dir, content)
        print(f"processing content: '{content_path}'")
        if os.path.isfile(content_path):
            print(f"FILE: copying '{content_path}' to '{destination_dir}'")
            shutil.copy(content_path, destination_dir)
        elif os.path.isdir(content_path):
            # make the destination subdirectory
            dest_sub_dir = os.path.join(destination_dir, content)
            os.mkdir(dest_sub_dir)
            print(f"DIRECTORY: created '{dest_sub_dir}' and recursively calling function")
            copy_all_contents(content_path, dest_sub_dir)

def main():
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy)
    copy_all_contents("static", "public")

main()
