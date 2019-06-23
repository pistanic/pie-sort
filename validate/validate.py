import searchHelp

def phn_primary(database, phn):
    dob_found_flag = False
    name_found_flag = False

    if searchHelp.is_in_df(database, 'PHN', phn) != True:
        print('Validation phn_primary - PHN ('+phn+') NOT FOUND IN DB')
        return False

    dob = searchHelp.get_dob_from_phn(database, phn)
    print('Validation phn_primary - dob: ' + dob)
    name = searchHelp.get_name_from_phn(database, phn)
    print('Validation phn_primary - name: ' + name)
