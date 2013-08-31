import os

def make_dir_for_file(filepath):
  folderpath = os.path.dirname(filepath)
  if not os.path.exists(folderpath):
    os.makedirs(folderpath)

