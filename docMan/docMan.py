# Document Managment module.
import tempfile
from os import listdir, remove
from os.path import isfile, join, splitext, basename
from shutil import rmtree
from pdf2image import convert_from_path

def get_file_list(path):
    fileList = [f for f in listdir(path) if isfile(join(path,f))]
    return fileList

def get_image_name(path):
    return get_file_list(path)

def delete_dir(path):
    rmtree(path)

def delete_file(path):
    remove(path)

def pdf2jpg(pdf_path, jpg_path):
    #PDF to JPG
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(pdf_path, dpi=200, output_folder=path) #PDF to PIL image output

    base_filename = splitext(basename(pdf_path))[0]+ '.jpg'
    for page in images_from_path:
        page.save(join(jpg_path, base_filename), 'JPEG')

    return base_filename
