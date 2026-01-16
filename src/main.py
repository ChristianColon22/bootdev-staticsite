import os
from copystatic import copy_files_recursive
from gencontent import generate_page
   

def main():
    copy_files_recursive("./static/", "./public/")
    root_dir = "content"
    out_dir = "public"
    for current_path, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.lower().endswith(".md"):
                full_path = os.path.join(current_path, filename)
                out_path = full_path.replace(root_dir, out_dir, 1) 
                out_path = out_path.rsplit(".",1)[0] + ".html"
                generate_page(full_path, "template.html", out_path)
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
