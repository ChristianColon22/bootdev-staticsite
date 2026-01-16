import sys
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
   

def main():
    # 1. Determine basepath
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    # Filesystem paths
    dir_path_content = "content"
    template_path = "template.html"
    dest_dir_path = "docs" 
    static_path = "static"
    copy_files_recursive(static_path, dest_dir_path)
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)

if __name__ == "__main__":
    main()
