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

from PIL import Image, ImageEnhance, ImageFilter


# INPUT: img_path - path to image that tesseract will process
#        txt_path - path to text file that tesseract will write data to.
# DESCRIPTION: Write ocr data to .csv file.
def extract_text(img_path, txt_path):
    # Returns text from image in form as string and then converts string into Pandas dataframe
    text = pytesseract.image_to_data(Image.open(img_path)) # Tesseract OCR
    # Write tab delimited string into txt file
    file = open(txt_path, 'w')
    file.write(text)
    file.close

# INPUT: img_path - path to image that tesseract will process
# OUTPUT: text - string of ocr data
def extract_string(img_path):
    # returns text from image in form as string
    text = pytesseract.image_to_string(Image.open(img_path))  # Tesseract OCR)
    return text

# INPUT: text_path - path to csv data
# OUTPUT: pandas dataframe created from csv file.
def text_to_dataframe(text_path):
    # Extract txt file into pandas dataframe and returns dataframe
    df = pd.read_csv(text_path, sep='\t',engine='python',quotechar="'"or'"')
    df = df.dropna()  # drop rows with text as nan
    #df.to_excel('tmp/ocr_data.xlsx') # Why do we need both? you can display csv with formatting.
    return df

# INPUT: dataframe
# OUTPUT: dataframe with all commas removed from the end of text.
# DESCRIPTION: format a dataframe to meet processing needs.
#              - Format the case of each text value (ROB, -> Rob,)
#              - Remove commas from the end (Rob, -> Rob)
def format_df(df):
    for index, row in df.iterrows():
        txt = row['text']
        stxt = str(txt)
        ftxt = stxt.title()
        df.at[index, 'text'] = ftxt
        if(ftxt.endswith(',')):
            ftxt = ftxt[:-1]
            df.at[index, 'text'] = ftxt
    print (df)
    return df

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
#        df - master ocr dataframe
# OUTPUT: dictonary - key = name : value = array of tesseract data
# DESCRIPTION: This function creates a candidate table given the phn list and formatted dataframe.
def create_phn_candidates(phns, formatted_df):
    phn_candidate_dict = {}
    for phn in phns:
        row_data = formatted_df.loc[df['text'] == phn]
        phn_candidate_dict[phn] = row_data.values

    return phn_candidate_dict

# INPUT: formatted_df dataframe of ocr output with comma striped.
#        name string - (first last)
# OUTPUT: success flag if name is found in ocr data
# DESCRIPTION:
def look_for_name(formatted_df, name):
    print ('look_for_name debug - validating '+name)
    first_last = name.split(' ', 1)

    # Create a copy of the dataframe with rows shifted up one
    formatted_df["next_name"] = formatted_df["text"].shift(1)

    # Create a copy of the dataframe with rows shifted down one
    formatted_df["previous_name"] = formatted_df["text"].shift(-1)
    first_idx = formatted_df.loc[formatted_df['text'] == first_last[0]].index[0]
    last_idx = formatted_df.loc[formatted_df['text'] == first_last[1]].index[0]
    idx = [first_idx, last_idx]
    names_df = formatted_df.loc[idx,['text','next_name','previous_name']]

    print(names_df)
    for i in range(len(idx)):
        text = names_df.loc[idx[i],'text']
        next_name = names_df.loc[idx[i],'next_name']
        lookup_name = text + ' ' + next_name
        if (lookup_name == name):
            print ('look_for_name debug - ' +name + " has been validated with: "+lookup_name)
            return True

        previous_name = names_df.loc[idx[i], 'previous_name']
        lookup_name = text + ' ' + previous_name
        if (lookup_name == name):
            print ('look_for_name debug - ' +name + " has been validated with: "+lookup_name)
            return True
