import os

def copy_directory(src_path, dest_path):
    if os.path.exists(src_path):
        src_tree = os.listdir(src_path)
        print(src_tree)
    if os.path.exists(dest_path):
        print(f"{dest_path} exists")
def main():
    print("Hello World")
    copy_directory("./static/", "./public/")

if __name__ == "__main__":
    main()
