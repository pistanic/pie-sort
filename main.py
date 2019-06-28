import preproc # for source see: preproc/
import ocr # for source see: ocr/
import nlp # for source see: nlp/
import ezRead
import docMan # four source see: docMan/
import searchHelp
import validate

def printf(name, value):
    print('+------------------------------------------------------------+')
    print('  Main Debug - '+name+':')
    print(value)
    print('+------------------------------------------------------------+')


def main():
    LOCAL_DIR = './'
    PDF_DIR = LOCAL_DIR+'PDF/'
    TMP_DIR = LOCAL_DIR+'tmp/'
    IMG_DIR = TMP_DIR+'img/'
    TXT_DIR = TMP_DIR+'txt/'
    patient_database = searchHelp.init_test_db()

    # Print Verification database
    printf('patient_database',patient_database)

    file_list = docMan.get_file_list(PDF_DIR)

    for file_ in file_list:
        # Print processing file
        printf('file_ in file_list', file_)
        image_name = docMan.pdf2jpg((PDF_DIR+file_), IMG_DIR) # store image in IMG_DIR
        # Print processing Image name
        printf('image_name', image_name)
        img_path = IMG_DIR+image_name

        # Preprocessing Stage
        preproc.pre_process(img_path)

        # OCR Stage
        txt_path = TXT_DIR+image_name.replace('.jpg','.txt')
        printf('txt_path',txt_path)
        ocr.extract_text(img_path, txt_path)
        ocr_df = ocr.text_to_dataframe(txt_path)
        ocr_str = ocr.extract_string(img_path)

        # AOI Masking Demo
        searchbox = searchHelp.define_search_box(850,500,850,500)# find values centered at pixels (X=850,Y=500) in a box with a width of +/-850 and height of +/-500
        aoi_df =searchHelp.return_inside_search_box(searchbox,ocr_df)
        printf('Area of Interest Dataframe',aoi_df)

        # NLP Stage
        # Create list of possible PHNs for patient
        PHNs = nlp.extract_PHN(ocr_df)
        printf('List of possible PHNs from document', PHNs)

        # Create list of possible names for patient
        hack_names = nlp.hack_extract_names(ocr_df)
        printf('List of possible names from document', hack_names)

        # Create list of possible date of births for patient
        DOBs = nlp.extract_DOB(ocr_str)
        printf('List of possible DOBs from document', DOBs)

        # Strip master dataframe of all commas after most processing has been done.
        formatted_df = ocr.format_df(ocr_df)
        printf('Formatted data frame', formatted_df)

        #Access confedence for the first instance of 'Contrast'
        #name_cand_dict[<Key>][<First/Last>][instance][data]
        #name_cand_dict = ocr.create_name_candidates(hack_names, comma_free_df)

        # Validate debug
        printf('PHN LIST: ',PHNs)
        for phn in PHNs:
            validate.phn_primary(formatted_df, patient_database, phn)



if __name__ == '__main__':
    main()
