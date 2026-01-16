import os 
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read in markdown
    with open(from_path, 'r') as f:
        markdown = f.read()
    # Read in template file
    with open(template_path, 'r') as f:
        template = f.read()
    # Convert markdown to html
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    # Replace title and content in template
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    # Write content to destination file 
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def extract_title(markdown):
    header_start_idx = markdown.find("# ")
    if header_start_idx == -1:
        raise ValueError("Title not found")
    header_end_idx = markdown.find("\n", header_start_idx)
    if header_end_idx == -1:
        return markdown[header_start_idx+2:]
    return markdown[header_start_idx+2:header_end_idx]