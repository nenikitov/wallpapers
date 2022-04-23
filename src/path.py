from os import path

root_folder = path.abspath(path.join(path.dirname( __file__ ), '..'))

def from_root(*paths):
    return path.abspath(path.join(root_folder, *paths))
