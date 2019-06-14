import pytesseract
import csv
import pandas as pd
import os
import time

from PIL import Image, ImageEnhance, ImageFilter


# INPUT: immg_path - path to immage that tesseract will process
#        txt_path - path to text file that tesseract will write data to.
# RETURN: pandas dataframe created from csv file.
def extract_text(img_path, txt_path):
     # returns text from image in form as string and then converts string into Pandas dataframe
    text = pytesseract.image_to_data(Image.open(img_path)) # Tesseract OCR
    # Write tab delimited string into txt file
    file = open(txt_path, 'w')
    file.write(text)
    file.close


def extract_string(img_path):
    # returns text from image in form as string
    text = pytesseract.image_to_string(Image.open(img_path))  # Tesseract OCR)
    return text

# INPUT: text_path - path to csv data
# RETURN: pandas dataframe created from csv file.
def text_to_dataframe(text_path):
    # Extract txt file into pandas dataframe and returns dataframe
    df = pd.read_csv(text_path, sep='\t')
    #df.to_excel('tmp/ocr_data.xlsx') # Why do we need both? you can display csv with formatting.
    return df

# INPUT: names - list of name strings
#        df - master ocr dataframe
# RETURN: dictonary - key = name : value = array of tesseract data
def create_name_candidates(names, df):
    name_candidate_dict = {}
    for name in names:
        row_data = df.loc[df['text'] == name]
        #TODO count the number of times name is added to the table.
        name_candidate_dict[name] = row_data.values

    return name_candidate_dict

# INPUT: phns - list of phn strings
#        df - master ocr dataframe
# RETURN: dictonary - key = name : value = array of tesseract data
def create_phn_candidates(phns, df):
    phn_candidate_dict = {}
    for phn in phns:
        row_data = df.loc[df['text'] == phn]
        #TODO count the number of times name is added to the table.
        phn_candidate_dict[phn] = row_data.values

    return phn_candidate_dict
