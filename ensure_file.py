import os
from sys import platform


def ensure_file(filename: str, default_write: str = ""):

    path = ""

    if platform == "linux" or platform == "linux2":
        path = os.path.expanduser(f"~/Desktop/{filename}")
    elif platform == "darwin":
        path = os.path.expanduser(f"~/Desktop/{filename}")
    elif platform == "win32":
        path = filename
    else:
        return -1

    if path == "":
        return -2

    if not os.path.exists(path):
        file = open(path, "w+")
        file.write(default_write)
        file.close()

    return path
