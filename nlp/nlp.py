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
from dateutil.parser import parse

# ******* Libraries not in use *************
#import stanfordnlp
#import nltk
#from nltk.corpus import stopwords
#stop = stopwords.words('english')


# INPUT: ocr_df - pandas dataframe of document OCR
# OUTPUT: possible_names - list of possible names
# DESCRIPTION: Searches OCR dataframe and returns list of PHNs for patient.
def extract_PHN(ocr_df):
    extraction_df = ocr_df.copy(deep=True)


    possible_PHNs = []

    #Strip everything except digits
    extraction_df['text'] = extraction_df['text'].str.replace("-","")
    extraction_df['text'] = extraction_df['text'].str.findall('(\d{7,11})')
    extraction_df['text'] = extraction_df['text'].apply(', '.join)

    # create boolean mask for numeric text in ocr_df
    df_digits_boo = extraction_df['text'].str.isdigit()
    df_mask = df_digits_boo == True

    df_digits = extraction_df['text'].loc[df_mask] # create new dataframe of only digits from OCR
    df_PHN = df_digits.loc[df_digits.str.len() >= 8]  # create dataframe of possible PHN (numbers with greater than or equal to 8 digits)
    possible_PHNs = list(df_digits.loc[(df_digits.str.len() > 4) & (df_digits.str.len() < 12)]) # create list of digits that are 5 to 12 characters in length

    return possible_PHNs

# INPUT: ocr_df - pandas dataframe of document OCR
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
# OUTPUT: possible_names - list of possible names
# DESCRIPTION: searches OCR dataframe and returns list of names for patient (HACK METHOD BECAUSE FUNCTION WILL FAIL IF ALL TEXT ARE UPPERCASE)
def hack_extract_names(ocr_df):
    possible_names = []

    for i in range(0, ocr_df.shape[0] - 1):
        if ocr_df['text'].iloc[i][0].isupper() and ocr_df['text'].iloc[i + 1][0].isupper():
            if ocr_df['text'].iloc[i][-1] == ",":
                # if format of name is 'Trudeau, Justin'
                if ocr_df['text'].iloc[i + 1][-1] == ",":
                    possible_names.append(ocr_df['text'].iloc[i + 1][:-1] + " " + ocr_df['text'].iloc[i])
                else:
                    possible_names.append(ocr_df['text'].iloc[i + 1][:-1] + " " + ocr_df['text'].iloc[i])
            else:
                # if format of name is 'Justin Trudeau'
                if ocr_df['text'].iloc[i + 1][-1] == ",":
                    possible_names.append(ocr_df['text'].iloc[i + 1][:-1] + " " + ocr_df['text'].iloc[i])
                else:
                    possible_names.append(ocr_df['text'].iloc[i] + " " + ocr_df['text'].iloc[i + 1])
    return possible_names


# INPUT: document - string of document text
# OUTPUT: tagged_words - array of text with parts of speech tagging
# DESCRIPTION: Tokenize string  and return array of parts of speech tagging
def pos_tagging(document):
    sentences = nltk.sent_tokenize(document)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    tagged_words = [nltk.pos_tag(word) for word in words]
    return tagged_words

# INPUT: document - string of document text
# OUTPUT: names - list of names identified from document text with NLTK NER function
# DESCRIPTION: output array of possible  names using NLTK Named Entity Recognition
def extract_names(document):
    names = []
    tagged = pos_tagging(document)
    named_ent = nltk.ne_chunk(tagged[0])
    for chunk in named_ent:
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() == 'PERSON':
                names.append(' '.join([c[0] for c in chunk])) # add possible names to array
    return names

