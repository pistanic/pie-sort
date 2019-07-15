#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: David Cheng                                           #
# Co-Authors:                                                   #
#                                                               #
#################################################################

# NLP module to find patient identifiers from OCR
import nltk
import spacy
import re
from collections import Counter
from dateutil.parser import parse

# INPUT: ocr_df - pandas dataframe of document OCR
#        ocr_str - string of document text
# OUTPUT: possible_names - list of possible names
# DESCRIPTION: Searches OCR dataframe and returns list of PHNs for patient.
def extract_PHN(ocr_df, ocr_str):
    extraction_df = ocr_df.copy(deep=True)

    possible_PHNs = []

    # METHOD 1: Find PHN through regular expressions to find "PHN" in ocr_string and return next word
    string_list = ocr_str.split()
    pattern_PHN = r'\bphn\b|\bid\b'
    p = re.compile(pattern_PHN, re.I)
    idx = [i for i, item in enumerate(string_list) if re.search(p, item)] # return index of "PHN" in string list

    for i in idx:
        if len(string_list[i]) < 5:
        # eg. if string_list[i] is "PHN:" or "PHN" then the PHN number is in the next index
            possible_PHNs.append(re.sub("\D", "", string_list[i+1])) # appends only numeric characters of word after "PHN" in list
        if len(string_list[i]) >= 5:
        # eg. if string_list[i] is "PHN:12345678" or "PHN1234578" then the PHN number is in the same index
            possible_PHNs.append(re.sub("\D", "", string_list[i])) # appends only numeric characters of word

    # METHOD 2: Find PHN through similar length digits
    #Strip everything except digits
    extraction_df['text'] = extraction_df['text'].str.replace("-","")
    extraction_df['text'] = extraction_df['text'].str.findall('(\d{7,11})')
    extraction_df['text'] = extraction_df['text'].apply(', '.join)

    # create boolean mask for numeric text in ocr_df
    df_digits_boo = extraction_df['text'].str.isdigit()
    df_mask = df_digits_boo == True

    df_digits = extraction_df['text'].loc[df_mask] # create new dataframe of only digits from OCR
    df_PHN = df_digits.loc[df_digits.str.len() >= 8]  # create dataframe of possible PHN (numbers with greater than or equal to 8 digits)
    similiar_length_digits = list(df_digits.loc[(df_digits.str.len() > 4) & (df_digits.str.len() < 12)]) # append list of digits that are 5 to 12 characters in length

    for digits in similiar_length_digits:
        possible_PHNs.append(digits)

    return possible_PHNs

# INPUT: ocr_str - string of document text
# OUTPUT: possible_DOBs - list of possible date of births
# DESCRIPTION: searches OCR dataframe and returns list of possible date of births for patient in ISO 8601 format (YYYY-MM-DD).
def extract_DOB(ocr_str): #TODO differentiate if 2019/01/05 is found from January 5th 2019 (good) or May 5th 2019 (bad)
    nlp = spacy.load("en_core_web_sm")
    unformatted_dates = []
    possible_DOBs = []

    doc = nlp(ocr_str)

    # use nlp to find dates in document
    for ent in doc.ents:
        if (ent.label_ == 'DATE'):
            unformatted_dates.append(ent)

    print('extract_DOB debug - DOB List:')
    print(unformatted_dates)

    # convert unformatted dates to ISO 8601 format (YYYY-MM-DD) using EAFP practice (easier to ask forgiveness than permission)

    for date in unformatted_dates:
        try:
            try:
                obj = parse(date.__str__())
            except OverflowError:
                print("extract_dob: overflow error converting: ")
                print(date)
                print()
                continue
            formatted_date = obj.strftime("%Y-%m-%d")
            possible_DOBs.append(formatted_date)
        except ValueError:
            print("extract_DOB debug - '" + date.__str__() + "' is not in a readable date format")

    return possible_DOBs

# INPUT: ocr_df - pandas dataframe of document OCR
# OUTPUT: names - list of names identified from rule based name extration and NLTK NER function
# DESCRIPTION: output array of possible names
def extract_names(ocr_df):
    possible_names = []
    ruled_names = rule_based_names(ocr_df)

    for name in ruled_names:
        word_tag = pos_tagging(name)
        named_ent = nltk.ne_chunk(word_tag[0])

        i = 0
        while i < len(named_ent):
            if type(named_ent[i]) == nltk.tree.Tree:
                if named_ent[i]._label == 'PERSON':
                    possible_names.append(name) # add possible names to array
            i = i + 1

    possible_names = sorted(possible_names, key=Counter(possible_names).get, reverse=True) # sort list by highest number of occurences
    possible_names = list(dict.fromkeys(possible_names)) # remove duplicates from list

    print("nlp.extract_names debug - # of rule based names: " + str(len(ruled_names)))
    print("nlp.extract_names debug - # after NER Filtering: " + str(len(possible_names)))
    return possible_names

# INPUT: ocr_df - pandas dataframe of document OCR
# OUTPUT: possible_names - list of possible names in Title Case
# DESCRIPTION: searches OCR dataframe and returns list of names based on if word is capitalized
def rule_based_names(ocr_df):
    capitalized_words = []

    for i in range(0, ocr_df.shape[0] - 1):
        if ocr_df['text'].iloc[i][0].isupper() and ocr_df['text'].iloc[i + 1][0].isupper():
            if ocr_df['text'].iloc[i][-1] == ",":
                # if format of name is 'Trudeau, Justin'
                if ocr_df['text'].iloc[i + 1][-1] == ",":
                    capitalized_words.append(ocr_df['text'].iloc[i + 1][:-1].title() + " " + ocr_df['text'].iloc[i][:-1].title())
                else:
                    capitalized_words.append(ocr_df['text'].iloc[i + 1].title() + " " + ocr_df['text'].iloc[i][:-1].title())
            else:
                # if format of name is 'Justin Trudeau'
                if ocr_df['text'].iloc[i + 1][-1] == ",":
                    capitalized_words.append(ocr_df['text'].iloc[i + 1][:-1].title() + " " + ocr_df['text'].iloc[i].title())
                else:
                    capitalized_words.append(ocr_df['text'].iloc[i].title() + " " + ocr_df['text'].iloc[i + 1].title())

    return capitalized_words

# INPUT: document - string of document text
# OUTPUT: tagged_words - array of text with parts of speech tagging
# DESCRIPTION: Tokenize string and return array of parts of speech tagging
def pos_tagging(document):
    sentences = nltk.sent_tokenize(document)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    tagged_words = [nltk.pos_tag(word) for word in words]
    return tagged_words
