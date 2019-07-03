#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Nicholas Forest                                       #
# Co-Authors:                                                   #
#                                                               #
#################################################################

import searchHelp
import nlp
import ocr

# INPUT: ocr_df - formatted dataframe of ocr data.
#        database - dataframe of the verification database.
#        phn - Personal Health number for verification.
# OUTPUT: true if the name or dob have been verified against the phn.
# DESCRIPTION: This function searchs for the name and DOB in the database given a phn.
def phn_primary(ocr_df, ocr_str, database, phn):
    success_flag = False
    if searchHelp.is_in_df(database, 'PHN', phn) != True:
        print('phn_primary debug - PHN ('+phn+') NOT FOUND IN DB')
        return success_flag

    name = searchHelp.get_name_from_phn(database, phn)
    if ocr.look_for_name(ocr_df, name):
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
