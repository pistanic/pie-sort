#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Nicholas Forest                                       #
# Co-Authors:                                                   #
#                                                               #
#################################################################
import pandas as pd

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
    df['text'] = df['text'].str.strip() # remove leading and trailing characters in Series/Index

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
        lookup_name = text + ' ' + str(next_name)
        if (lookup_name == name):
            print ('look_for_name debug - ' +name + " has been validated with: "+lookup_name)
            return True

        previous_name = names_df.loc[idx[i], 'previous_name']
        lookup_name = text + ' ' + str(previous_name)
        if (lookup_name == name):
            print ('look_for_name debug - ' +name + " has been validated with: "+lookup_name)
            return True

# INPUT: ocr_df - formatted dataframe of ocr data.
#        database - dataframe of the verification database.
#        phn - Personal Health number for verification.
# OUTPUT: true if the name or dob have been verified against the phn.
# DESCRIPTION: This function searchs for the name and DOB in the database given a phn.
def phn_primary(df_list, phn):
    # These can be moved to a larger validation control loop
    # One call from main to validate.
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

# INPUT: df_list - List of data frames passed from main
#        name - name to validate
# OUTPUT:
# DESCRIPTION:
def name_primary(df_list, personal_id):
    # These can be moved to a larger validation control loop
    # One call from main to validate.
    database = df_list[2]
    name_list = personal_id[0]
    PHNs = personal_id[1]

    # Create empty df to be filled with all hits.
    first_hits = pd.DataFrame(columns=database.columns.values)
    mid_hits = pd.DataFrame(columns=database.columns.values)
    last_hits = pd.DataFrame(columns=database.columns.values)
    for name in name_list:
        # Split names to first, middle (optional), last names.
        name = name.split()
        # Check assumption
        if len(name) > 3:
            print('Validation Error in Name-Primary: More than 3 sub names within name.')
            continue
        for sub_name in name:
            # Format subnames
            sub_name = sub_name.title()
            if(sub_name.endswith(',') or sub_name.endswith('.')):
                sub_name = sub_name[:-1]
            try:
                hit_idx = database.loc[database['First_Name'] == sub_name].index[0]
                first_hits.loc[database.index[hit_idx]] = database.iloc[hit_idx]
            except IndexError:
                pass
                #print(sub_name+' is not a first name in the database.')
            try:
                hit_idx = database.loc[database['Middle_Name'] == sub_name].index[0]
                mid_hits.loc[database.index[hit_idx]] = database.iloc[hit_idx]
            except IndexError:
                pass
                #print(sub_name+' is not a middle name in the database.')
            try:
                hit_idx = database.loc[database['Last_Name'] == sub_name].index[0]
                last_hits.loc[database.index[hit_idx]] = database.iloc[hit_idx]
            except IndexError:
                pass
                #print(sub_name+' is not a last name in the database.')

    # Merge all hits df as long as they are not empty.
    # If first or last is empty, set the hits_df to first OR last. Middle will be neglected.
    merge_col = ['First_Name', 'Middle_Name', 'Last_Name', 'PHN']
    hits_df = pd.merge(first_hits, last_hits, on=merge_col, how='outer')
    hits_df = pd.merge(hits_df, mid_hits, on=merge_col, how='outer')

    print('validation debug- Hits_df:')
    print(hits_df)

    # if this df is empty all hits in first, mid, last were unique.
    if hits_df.empty:
        print("validation debug - NO HITS! ALL DF EMPTY")
        return False

     # check hits df for phn to confirm
    validated = False
    for phn in PHNs:
        tmp = hits_df.loc[hits_df['PHN'] == phn]
        if not tmp.empty:
            validated = True
            break

    if validated:
        print('Validation debug name_primary - SUCCESS')
        return True
    else:
        print('Validation debug name_primary - FAILED - PHN not found in hits df')
        return False

def validate(df_list, personal_id, database):
    # TODO Fix pass database seperatly. This is a hack cuz Im tired and
    # want to finish this refactor
    # should also make nameing more consistent... from main input is:
    # ocr_list and id_list
    df_list.append(database)

    validated = False
    # TODO return validated name and phn.
    valid_phn = None
    print("***** ATTEMPTING PHN_PRIMARY VALIDATION *****")
    for phn in personal_id[1]:
        if phn_primary(df_list, phn):
            validated = True
            valid_phn = phn
            break
    if(not validated):
        print("***** PHN_PRIMARY VALIDATION FAILED *****")
        print()
        print("***** ATTEMPTING NAME_PRIMARY VALIDATION *****")
        if name_primary(df_list, personal_id):
            validated = True
        else:
            print("***** NAME_PRIMARY VALIDATION FAILED *****")
            # Third stage validation
            pass

    return validated
