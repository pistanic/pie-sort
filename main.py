import preproc # for source see: preproc/
import ocr # for source see: ocr/
import nlp # for source see: nlp/
import docMan # for source see: docMan/
import ezRead
from enum import Enum

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
        print(txt_path)
        ocr.extract_text(img_path, txt_path)
        ocr_df = ocr.text_to_dataframe(txt_path)

        # NLP Stage
        #PHN = nlp.simple_nlp(nlp.extract_PHN(ocr_df))
        #print(PHN)
        #name_list = ['Andrea', 'Stacey'] # This is for a demo. This list will be returned by a validate names function.

        # Strip master dataframe of all commas after most processing has been done.
        comma_free_df = ocr.strip_df_commas(ocr_df)

        name_list = ['Contrast Smailys', 'Stacey Lynn'] # This is for a demo. This list will be returned by a validate names function.
        name_cand_dict = ocr.create_name_candidates(name_list, comma_free_df)
        # Access confedence for the first instance of 'Contrast'
        # name_cand_dict[<Key>][<First/Last>][instance][data]
        print(name_cand_dict['Contrast Smailys'][ezRead.first_name()][0][ezRead.conf()])



    #text = ocr.simple_ocr("images/example.png");
    #print("Tesseract OCR output:")
    #print(text)
    #print("Stanford Nlp output:")
    #nlp.simple_nlp(text);

if __name__ == '__main__':
	main()
