#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Nicholas Forest                                       #
# Co-Authors:                                                   #
#                                                               #
#################################################################

import searchHelp
import nlp

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
    return df

# INPUT: formatted_df - dataframe of ocr output with comma striped.
#        name string - (first last)
# OUTPUT: Boolean success flag if name is found in ocr data
# DESCRIPTION: Look for name in formatted dataframe
def look_for_name(formatted_df, name):
    print ('look_for_name debug - validating '+name)
    first_last = name.split(' ', 1)

    # Create a copy of the dataframe with rows shifted up one
    formatted_df["next_name"] = formatted_df["text"].shift(1)

    # Create a copy of the dataframe with rows shifted down one
    formatted_df["previous_name"] = formatted_df["text"].shift(-1)
    try:
        first_idx = formatted_df.loc[formatted_df["text"] == first_last[0]].index[0]
    except IndexError: #FIXME THIS IS A HACK
        return False
    try:
        last_idx = formatted_df.loc[formatted_df["text"] == first_last[1]].index[0]
    except IndexError: #FIXME THIS IS A HACK
        return False

    idx = [first_idx, last_idx]
    names_df = formatted_df.loc[idx,['text','next_name','previous_name']]

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

# INPUT: ocr_df - formatted dataframe of ocr data.
#        database - dataframe of the verification database.
#        phn - Personal Health number for verification.
# OUTPUT: true if the name or dob have been verified against the phn.
# DESCRIPTION: This function searchs for the name and DOB in the database given a phn.
def phn_primary(df_list, phn):
    ocr_df = format_df(df_list[0])
    ocr_str = df_list[1]
    database = df_list[2]

    success_flag = False
    if searchHelp.is_in_df(database, 'PHN', phn) != True:
        print('phn_primary debug - PHN ('+phn+') NOT FOUND IN DB')
        return success_flag

    name = searchHelp.get_name_from_phn(database, phn)
    if look_for_name(ocr_df, name):
        print('phn_primary debug - name validated')
        success_flag = True

    dob = searchHelp.get_dob_from_phn(database, phn)
    if dob == "Nan-Nan-Nan":
        print('phn_primary debug - NO DOB FOUND IN DB')
        return success_flag

    for doc_dob in nlp.extract_DOB(ocr_str):
        print('phn_primary debug - checking database DB: '+dob+' against ocr dob: '+doc_dob)
        if dob == doc_dob:
            success_flag = True
            print('phn_primary debug - DOB validated')

    return success_flag
