#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: David Cheng                                           #
# Co-Authors: Nicholas Forest                                   #
#                                                               #
#################################################################

import pytesseract
import csv
import pandas as pd
import os
import time
import numpy as np
import docMan

from PIL import Image, ImageEnhance, ImageFilter

# INPUT: img_path - path to image that tesseract will process
#        txt_path - path to text file that tesseract will write data to.
# OUTPUT: None
# DESCRIPTION: writes OCR data to a text file in form of tab delimited csv.
def extract_text(img_path, txt_path):
    file_list = docMan.get_file_list(img_path)
    file_list.sort()
    i = 1
    for file_ in file_list:
        text = pytesseract.image_to_data(Image.open(img_path+'/'+file_)) # Tesseract OCR
        # Write tab delimited string into txt file
        file = open(txt_path+'/'+file_.replace('.jpg','.txt'), 'w')
        file.write(text)
        file.close

# INPUT: text_path - path to csv data
# OUTPUT: pandas dataframe created from csv file
# DESCRIPTION: read tab delimited csv text file of OCR data and returns as pandas dataframe.
def text_to_dataframe(text_path):
    file_list = docMan.get_file_list(text_path)
    file_list.sort()
    dataframe_list = []
    for i, file_ in enumerate(file_list):
        ocr_df = pd.read_csv(text_path+'/'+file_, sep='\t', engine='python', quoting=csv.QUOTE_NONE, encoding='utf-8')
        ocr_df = ocr_df.dropna()  # drop rows with text as nan
        ocr_df['page'] = pd.Series(i+1, index=ocr_df.index)
        dataframe_list.append(ocr_df)
    ocr_df_Final = pd.concat(dataframe_list, ignore_index=True)
    return ocr_df_Final

# INPUT: img_path - path to image that tesseract will process
# OUTPUT: text - string of ocr data
# DESCRIPTION: returns text from image in form as string
def extract_string(img_path):
    file_list = docMan.get_file_list(img_path)
    file_list.sort()
    text = ''
    for file_ in file_list:
        text = text + pytesseract.image_to_string(Image.open(img_path+'/'+file_)) + ' '      # Tesseract OCR)
    return text

# INPUT: names - list of name strings
#        df - master ocr dataframe
# OUTPUT: dictonary - key = name ("First Last")  : value = 3d array of tesseract data
# DATA REPRESENTATION:
#
# Z- Dimenstion first / last name
#            +-----------------------------------------------------------------------------------------------------------/|
#  last     /                                                                                                           / |
#          /---------------------------------------------------------------------------------------------------------- /| |
# first   /   0         1           2         3         4           5        6     7      8       9       10     11   / | |
#         +-------+----------+-----------+---------+----------+----------+------+-----+-------+--------+------+------+  | |
#         | level | page_num | block_num | par_num | line_num | word_num | left | top | width | height | conf | text |  | |
#instance +-------+----------+-----------+---------+----------+----------+------+-----+-------+--------+------+------+  | |
#   0     |       |          |           |         |          |          |      |     |       |        |      |      |  | |
#         +-------+----------+-----------+---------+----------+----------+------+-----+-------+--------+------+------+  | |
#   1     |       |          |           |         |          |          |      |     |       |        |      |      |  | |
#         +-------+----------+-----------+---------+----------+----------+------+-----+-------+--------+------+------+  | |
#   ...   |       |          |           |         |          |          |      |     |       |        |      |      |  |/
#         +-------+----------+-----------+---------+----------+----------+------+-----+-------+--------+------+------+  /
#   N     |       |          |           |         |          |          |      |     |       |        |      |      | /
#         +-------+----------+-----------+---------+----------+----------+------+-----+-------+--------+------+------+/


# INPUT: names - list of potential names for patient
#        formatted_df - formatted pandas dataframe of OCR data
# OUTPUT: name_candidate_dict - dictonary - key = name : value = array of tesseract data
# DESCRIPTION: This function creates a candidate table given the names list and formatted dataframe.
def create_name_candidates(names, formatted_df):
    name_candidate_dict = {}
    for name in names:
        names_data_arr = []
        temp = []
        first_last = name.split(' ', 1)
        for half_name in first_last:
            row_data = formatted_df.loc[df['text'] == half_name]
            temp = np.stack(row_data.values)
            names_data_arr.append(temp)

        name_candidate_dict[name] = names_data_arr

    return name_candidate_dict

# INPUT: phns - list of phn strings
#        formatted_df - formatted pandas dataframe of OCR data
# OUTPUT: dictonary - key = name : value = array of tesseract data
# DESCRIPTION: This function creates a candidate table given the phn list and formatted dataframe.
def create_phn_candidates(phns, formatted_df):
    phn_candidate_dict = {}
    for phn in phns:
        row_data = formatted_df.loc[df['text'] == phn]
        phn_candidate_dict[phn] = row_data.values

    return phn_candidate_dict

