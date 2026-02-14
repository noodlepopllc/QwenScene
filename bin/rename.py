
import os

def rename_jpgs(path):
    files = [f for f in os.listdir(path) if f.lower().endswith(".jpg")]

    # sort by modification time instead of filename
    files.sort(key=lambda f: os.path.getmtime(os.path.join(path, f)))

    for i, filename in enumerate(files, start=1):
        new_name = f"{i}.jpg"
        os.rename(os.path.join(path, filename),
                  os.path.join(path, new_name))

if __name__ == '__main__':
    import sys
    rename_jpgs(sys.argv[1])

