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

def text_to_dataframe(text_path):
    # Extract txt file into pandas dataframe and returns dataframe
    df = pd.read_csv(text_path, sep='\t')
    #df.to_excel('tmp/ocr_data.xlsx') # Why do we need both? you can display csv with formatting.
    return df
