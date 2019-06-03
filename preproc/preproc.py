# Preprocessing functions to prepare pdf for ocr/nlp

from pdf2image import convert_from_path

def pdftojpg(pdf_path, jpg_path):
    #PDF to JPG

    images_from_path = convert_from_path(pdf_path, dpi=200, output_folder=jpg_path) #PDF to PIL image output

    return images_from_path
