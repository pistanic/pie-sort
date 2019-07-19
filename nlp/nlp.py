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
import pandas as pd

# INPUT: string - string of text
# OUTPUT: Number of digits in string of text
# DESCRIPTION: Given a string function returns number of digits ie: abc-123456 returns 6
def count_digits(string):
    return sum(item.isdigit() for item in string)

# INPUT: ocr_df - pandas dataframe of document OCR
#        ocr_str - string of document text
# OUTPUT: possible_names - list of possible names
# DESCRIPTION: Searches OCR dataframe and returns list of PHNs for patient.
def extract_PHN(ocr_df, ocr_str):
    extraction_df = ocr_df.copy(deep=True)

    possible_PHNs = []

    # Step 1: Find PHN through regular expressions to find "PHN" in ocr_string and return next word
    string_list = ocr_str.split()
    pattern_PHN = r'\bphn\b|\bid\b|\hin\b|\hn\b'
    p = re.compile(pattern_PHN, re.I) # re.I ignores case
    idx = [i for i, item in enumerate(string_list) if re.search(p, item)] # return index of "PHN" in string list

    for i in idx:
        if len(string_list[i]) < 5:
        # eg. if string_list[i] is "PHN:" or "PHN" then the PHN number is in the next index
            possible_PHNs.append(re.sub("\D", "", string_list[i+1])) # appends only numeric characters of word after "PHN" in list
        if len(string_list[i]) >= 5:
        # eg. if string_list[i] is "PHN:12345678" or "PHN1234578" then the PHN number is in the same index
            possible_PHNs.append(re.sub("\D", "", string_list[i])) # appends only numeric characters of word

    # Step 2: Find PHN through similar length digits ie. any digit more than 4 characters and less than 12

    # ************************************** NEW NEEDS TO BE TESTED IN CLINIC **************************************

    # Case where PHN is PHN:12345678-00, 12345678-00, PHN:12345678_000, etc
    count_df = pd.DataFrame(columns=['digit_count'])

    count_df['digit_count'] = extraction_df['text'].apply(count_digits)  # count number of digits ie. PHN123456 returns 6
    count_df = count_df.join(extraction_df)

    count_df = count_df[count_df['digit_count'] > 9]
    for i in range(len(count_df)):
        if len(count_df['text'].iloc[i]) - count_df['text'].iloc[i].rfind('-') == 4:  # find placement of last "-"
            possible_PHNs.append(re.sub("\D", "", count_df['text'].iloc[i][:-4]))  # strip anything after last "-" and append only characters to list
        if len(count_df['text'].iloc[i]) - count_df['text'].iloc[i].rfind('-') == 3:
            possible_PHNs.append(re.sub("\D", "", count_df['text'].iloc[i][:-3]))
        if len(count_df['text'].iloc[i]) - count_df['text'].iloc[i].rfind('_') == 4:
            possible_PHNs.append(re.sub("\D", "", count_df['text'].iloc[i][:-4]))
        if len(count_df['text'].iloc[i]) - count_df['text'].iloc[i].rfind('_') == 3:
            possible_PHNs.append(re.sub("\D", "", count_df['text'].iloc[i][:-3]))

    # ********************************************** END OF NEW **********************************************

    # Strip everything except digits
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

    possible_PHNs = sorted(possible_PHNs, key=Counter(possible_PHNs).get, reverse=True) # sort list by highest number of occurences
    possible_PHNs = list(dict.fromkeys(possible_PHNs)) # remove duplicates from list

    return possible_PHNs

# INPUT: ocr_str - string of document text
# OUTPUT: possible_DOBs - list of possible date of births
# DESCRIPTION: searches OCR dataframe and returns list of possible date of births for patient in ISO 8601 format (YYYY-MM-DD).
def extract_DOB(ocr_str): #TODO differentiate if 2019/01/05 is found from January 5th 2019 (good) or May 5th 2019 (bad)
    nlp = spacy.load("en_core_web_sm")
    unformatted_dates = []
    possible_DOBs = []

    # Step 1: Find DOB through regular expressions to find DOB pattern in ocr_string and use nlp to find date in words after
    string_list = ocr_str.split()
    pattern_date = r'\bdob\b|\bDate of Birth\b|\bbirth date\b|\bbirthday\b|\bbd\b'
    p = re.compile(pattern_date, re.I) # re.I ignores case
    idx = [i for i, item in enumerate(string_list) if re.search(p, item)]  # return index of pattern in string list

    for i in idx:
        index_date = re.sub(p, "", string_list[i]) # eg. 'DOB:04-Jul-1943' -> :04-Jul-1943
        if index_date: # if not empty string
            if index_date[0] == ":" or "-" or ";": # eg. :04-Jul-1943
                index_date = index_date[1:] # remove first character

        unformatted_dates.append(index_date)  # append date
        unformatted_dates.append(index_date+" "+string_list[i+1]+" "+string_list[i+2])
        unformatted_dates.append(string_list[i+1])
        unformatted_dates.append(string_list[i+1]+" "+string_list[i+2]+" "+string_list[i+3])


    # Step 2: Find DOB through natural language processing of doc string
    doc = nlp(ocr_str)

    for ent in doc.ents:
        if (ent.label_ == 'DATE'):     # use nlp to find dates in document
            unformatted_dates.append(ent) # append date

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

    possible_DOBs = sorted(possible_DOBs, key=Counter(possible_DOBs).get, reverse=True)  # sort list by highest number of occurences
    possible_DOBs = list(dict.fromkeys(possible_DOBs))  # remove duplicates from list

    return possible_DOBs

# INPUT: ocr_df - pandas dataframe of document OCR
# OUTPUT: names - list of names identified from rule based name extration and NLTK NER function
# DESCRIPTION: output array of possible names
def extract_names(ocr_df):
    possible_names = []

    # Find names through rule based on capitalized letters filtered with named entity recognition
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

    # Step 1: use regular expressions to find pattern in ocr_df and remove ie. Nom:David -> David
    pattern_name = r'\bname\b|\bnom\b|\bpatient\b'
    p = re.compile(pattern_name, re.I) # re.I ignores case
    ocr_df['text'] = ocr_df['text'].str.replace(p, ' ', regex=True) # remove pattern
    ocr_df['text'] = ocr_df['text'].str.replace('\W', ' ') # remove special characters

    for i in range(0, ocr_df.shape[0]-2):
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

def processing(ocr_list):
    ocr_df = ocr_list[0]
    ocr_str = ocr_list[1]

    PHNs = extract_PHN(ocr_df, ocr_str)
    print('Nlp processing debug - List of possible PHNs from document:')
    print(PHNs)

    # Create list of possible names for patient
    names = extract_names(ocr_df)
    print('Nlp processing debug - List of possible names from document:')
    print(names)

    # Create list of possible date of births for patient
    DOBs = extract_DOB(ocr_str)
    print('Nlp processing debug - List of possible DOBs from document:')
    print(DOBs)

    return [names,PHNs, DOBs]

