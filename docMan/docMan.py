#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Nicholas Forest                                       #
# Co-Authors:                                                   #
#                                                               #
#################################################################

# Document Managment module.
import tempfile
from os import listdir, remove,makedirs
from os.path import isfile, join, splitext, basename, exists
from shutil import rmtree
from pdf2image import convert_from_path

# INPUT: Path to files
# OUTPUT: List of files in path
def get_file_list(path):
    fileList = [f for f in listdir(path) if isfile(join(path,f))]
    return fileList

# INPUT: Path to image folder
# OUTPUT: list of images in folder
def get_image_name(path):
    return get_file_list(path)

# INPUT: Path to be removed
def delete_dir(path):
    rmtree(path)

# INPUT: Path to to removed
def delete_file(path):
    remove(path)

# INPUT: pdf_path - path to PDF
#        jpg_path - path to store .jpg
# OUTPUT: base_filename - <file_name>.jpg
# DESCRIPTION: This function converts a PDF to JPG immage format.
def pdf2jpg(pdf_path, jpg_path):
    #PDF to JPG
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(pdf_path, dpi=200, output_folder=path) #PDF to PIL image output

    base_filename = splitext(basename(pdf_path))[0]

    try:
        makedirs(join(jpg_path, base_filename))
    except:
        print('Directory already exists')

    i = 1
    for page in images_from_path:

        page.save(join(jpg_path,base_filename,base_filename +'_page'+str(i)+'.jpg'), 'JPEG')
        i = i + 1

    print('pdf2jpg debug - base_filename: ',base_filename)

    return base_filename
