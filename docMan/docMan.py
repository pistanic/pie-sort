# Document Managment module.
from os import listdir
from os.path import isfile, join
from shutil import rmtree

def get_file_list(path):
    fileList = [f for f in listdir(path) if isfile(join(path,f))]
    return fileList

def get_image_name(path):
    return get_file_list(path)

def delete_dir(path):
    rmtree(path)

