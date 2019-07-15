import preproc # for source see: preproc/
import ocr # for source see: ocr/
import nlp # for source see: nlp/
import ezRead
import docMan # four source see: docMan/
import searchHelp
import validate
from os import makedirs

def printf(name, value):
    print('+------------------------------------------------------------+')
    print('  Main Debug - '+name+':')
    print(' '+str(value))
    print('+------------------------------------------------------------+')


def main():
    LOCAL_DIR = './'
    PDF_DIR = LOCAL_DIR+'PDF/'
    TMP_DIR = LOCAL_DIR+'tmp/'
    SORT_DIR = LOCAL_DIR+'pd/'
    IMG_DIR = TMP_DIR+'img/'
    TXT_DIR = TMP_DIR+'txt/'
    patient_database = searchHelp.init_test_db()

    # Print Verification database
    printf('patient_database',patient_database)

    file_list = docMan.get_file_list(PDF_DIR)

    # Validation Stats
    num_val_docs = 0
    failed_docs = []
    validated_docs = []
    # Main processing loop
    for file_ in file_list:
        # Print processing file
        printf('file_ in file_list', file_)
        image_name = docMan.pdf2jpg((PDF_DIR+file_), IMG_DIR) # store image in IMG_DIR
        # Print processing Image name
        print('image_name', image_name)
        img_path = IMG_DIR+image_name

        # Preprocessing Stage
        #img_path = preproc.pre_process(img_path)

        # OCR Stage
        printf('txt_dir + img_name',TXT_DIR+image_name)

        try:
            makedirs(TXT_DIR+image_name.replace('.jpg',''))
        except:
           print('Text Directory already exists')

        printf('TXT_DIR+image_name.replace(.jpg)',TXT_DIR+image_name.replace('.jpg',''))

        txt_path = TXT_DIR+image_name.replace('.jpg','')
        printf('txt_path',txt_path)
        ocr.extract_text(img_path, txt_path)
        ocr_df = ocr.text_to_dataframe(txt_path)
        printf('ocr_df:', ocr_df)
        ocr_str = ocr.extract_string(img_path)

        # AOI Masking Demo
        PHN_AOI_demo = 'Sidney'
        aoi_df = searchHelp.PHN_Document_Box_Search(PHN_AOI_demo,ocr_df,500,500)
        printf('Area of Interest Dataframe', aoi_df)

        # NLP Stage
        # Create list of possible PHNs for patient
        PHNs = nlp.extract_PHN(ocr_df)
        printf('List of possible PHNs from document', PHNs)

        # Create list of possible names for patient
        names = nlp.extract_names(ocr_df)
        printf('List of possible names from document', names)

        # Create list of possible date of births for patient
        DOBs = nlp.extract_DOB(ocr_str)
        printf('List of possible DOBs from document', DOBs)

        # Strip master dataframe of all commas after most processing has been done.
        #printf('Formatted data frame', formatted_df)

        #Access confedence for the first instance of 'Contrast'
        #name_cand_dict[<Key>][<First/Last>][instance][data]
        #name_cand_dict = ocr.create_name_candidates(hack_names, comma_free_df)

        # FIXME Valdiation should be moved to a control loop inside validation
        # module.

        #Validate debug
        df_list = [ocr_df, ocr_str, patient_database, hack_names]
        printf('PHN LIST: ',PHNs)
        validated = False;
        valid_phn = 0;
        for phn in PHNs:
            if validate.phn_primary(df_list, phn):
                num_val_docs += 1
                validated = True
                valid_phn = phn
                break

        # Name Primary validation is working.
        # TODO move validation to its own control loop.
        #if validate.name_primary(df_list, PHNs):
        #    num_val_docs += 1
        #    validated = True


        if (validated):
            dist_path = SORT_DIR+valid_phn+'/'+file_
            source_path = PDF_DIR+file_
            docMan.sort(source_path, dist_path)
            validated_docs.append(file_,)
            # DEBUG OPERATION! #
            # Move files back to PDF folder to aviod reverting manually.
            docMan.un_sort(dist_path, source_path)
            # ---------------- #
        else:
            failed_docs.append(file_)

    printf('Number of Validated Documents out of '+str(len(file_list)),num_val_docs)
    printf('Accuracy', (num_val_docs/len(file_list)))
    printf('Validated Documents',validated_docs)
    printf('Failing Documents',failed_docs)


if __name__ == '__main__':
    main()
