# Preprocessing functions to prepare pdf for ocr/nlp

from pdf2image import convert_from_path

def pdftojpg(pdf_path):

    images_from_path = conver_from_path(pdf_path, outputfolder='/home/pie/pie-sort/JPEGs')

    return jpg_path
