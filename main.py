import preproc # for source see: preproc/
import ocr # for source see: ocr/
import nlp # for source see: nlp/
import ezRead
import docMan # four source see: docMan/
import IMGSearchHelpers

def printf(name, value):
    print('+------------------------------------------------------------+')
    print('  Printing Variable: '+name)
    print(value)
    print('+------------------------------------------------------------+')

patient_database = IMGSearchHelpers.init_test_db()

printf('patient_database',patient_database)

def main():
    LOCAL_DIR = './'
    PDF_DIR = LOCAL_DIR+'PDF/'
    TMP_DIR = LOCAL_DIR+'tmp/'
    IMG_DIR = TMP_DIR+'img/'
    TXT_DIR = TMP_DIR+'txt/'

    # Preprocessing Stage
    file_list = docMan.get_file_list(PDF_DIR)
    for file_ in file_list:

        print(file_)
        image_name = docMan.pdf2jpg((PDF_DIR+file_), IMG_DIR) # store image in IMG_DIR
        print(image_name)
        img_path = IMG_DIR+image_name

        # OCR Stage
        txt_path = TXT_DIR+image_name.replace('.jpg','.txt')
        print('txt_path',txt_path)
        ocr.extract_text(img_path, txt_path)
        ocr_df = ocr.text_to_dataframe(txt_path)
        ocr_str = ocr.extract_string(img_path)

        # NLP Stage
        #PHN = nlp.simple_nlp(nlp.extract_PHN(ocr_df))
        #print(PHN)

        # Strip master dataframe of all commas after most processing has been done.
        comma_free_df = ocr.strip_df_commas(ocr_df)

        name_list = ['Contrast Smailys', 'Stacey Lynn'] # This is for a demo. This list will be returned by a validate names function.
        name_cand_dict = ocr.create_name_candidates(name_list, comma_free_df)
        # Access confedence for the first instance of 'Contrast'
        # name_cand_dict[<Key>][<First/Last>][instance][data]
        print('name_cand_dict confidence of first name of first instance for Contrast Samilys',name_cand_dict['Contrast Smailys'][ezRead.first_name()][0][ezRead.conf()])

        # test validate
        for name in name_list:
            first_name = name_cand_dict[name][ezRead.first_name()][0][ezRead.text()]
            last_name = name_cand_dict[name][ezRead.last_name()][0][ezRead.text()]
            # read the text for the first instane of each name
            if(patient_database['First_Name'].str.contains(first_name).any()):
                printf("following name has been validated as first name", first_name)

            if(patient_database['Last_Name'].str.contains(last_name).any()):
                print("following name has been validated as last name", last_name)

        hack_names = nlp.hack_extract_names(ocr_df)
        nlp_names = nlp.extract_names(ocr_str)
        printf('nlp_names', nlp_names)
       #nlptext = nlp.simple_nlp(ocr_df['text'])

    #text = ocr.simple_ocr("images/example.png");
    #print("Tesseract OCR output:")
    #print(text)
    #print("Stanford Nlp output:")
    #nlp.simple_nlp(text);

if __name__ == '__main__':
	main()
