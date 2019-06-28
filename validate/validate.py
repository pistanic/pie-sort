#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Nicholas Forest                                       #
# Co-Authors:                                                   #
#                                                               #
#################################################################

import searchHelp
import ocr

def phn_primary(ocr_df, database, phn):
    success_flag = False

    if searchHelp.is_in_df(database, 'PHN', phn) != True:
        print('phn_primary debug - PHN ('+phn+') NOT FOUND IN DB')
        return False

    dob = searchHelp.get_dob_from_phn(database, phn)
    print('phn_primary debug - dob: ' + dob)

    name = searchHelp.get_name_from_phn(database, phn)
    if ocr.look_for_name(ocr_df, name):
        print('phn_primary debug: name validated')
        success_flag = True

    return success_flag
