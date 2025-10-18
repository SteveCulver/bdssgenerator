import os
import shutil
from pathlib import Path
from src.block_markdown import markdown_to_html_node

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

def extract_title(markdown):
    if markdown is None or markdown == "":
        raise ValueError("markdown is None or empty string")
    
    lines = markdown.splitlines()
    header = ""
    for l in lines:
        if l.startswith("# "):
            header = l.split(" ")[1].strip()
            break
    if header == "":
        raise Exception("no h1 header found")
    return header



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")

    from_path = os.path.abspath(from_path)
    if not os.path.exists(from_path):
        raise ValueError(f"from_path: '{from_path}' doesn't exist")
    template_path = os.path.abspath(template_path)
    if not os.path.exists(template_path):
        raise ValueError(f"template_path: '{template_path}' doesn't exist")
    dest_path = os.path.abspath(dest_path)

    # Read the markdown file at from_path and store the contents in a variable
    markdown_file = ""
    with open(from_path) as f:
        markdown_file = f.read()

    # Read the template file at template_path and store the contents in a variable
    template_file = ""
    with open(template_path) as f:
        template_file = f.read()

    # Use markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string
    html = markdown_to_html_node(markdown_file).to_html()

    # Use the extract title function to grab the title on the page
    title = extract_title(markdown_file)

    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html)

    # Write the new full HTML page to a file at dest_path, creating any necessary directories if they don't exist
    path = Path(dest_path)
    os.makedirs(path.parent, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(template_file)

    

def main():
    # Delete anything in public and copy all static files from static to public
    copy_all_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()
