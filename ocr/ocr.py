import pytesseract
import csv
import pandas as pd
import os
import time

from PIL import Image, ImageEnhance, ImageFilter


def extract_text(immg_path, txt_path):
     # returns text from image in form as string and then converts string into Pandas dataframe

    text = pytesseract.image_to_data(Image.open(immg_path)) # Tesseract OCR

    # Write tab delimited string into txt file
    file = open(txt_path, 'w')
    file.write(text)
    file.close

def text_to_dataframe():
    # Extract txt file into pandas dataframe and returns dataframe
    df = pd.read_csv('./tmp/txt/ocr_data.txt', sep='\t')
    df.to_excel('tmp/ocr_data.xlsx') # **** saves into excel TO BE DELETED LATER ****
    return df
