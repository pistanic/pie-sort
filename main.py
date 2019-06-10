import preproc # for source see: preproc/
import ocr # for source see: ocr/
import nlp # for source see: nlp/
import docMan # four source see: docMan/

def main():
    LOCAL_DIR = './'
    PDF_DIR = LOCAL_DIR+'PDF/'
    TMP_DIR = LOCAL_DIR+'tmp/'
    IMG_DIR = LOCAL_DIR+'img/'
    # Preprocessing Stage

    file_list = docMan.get_file_list(PDF_DIR)
    for file_ in file_list:
        image_name = docMan.pdf2jpg((PDF_DIR+file_), IMG_DIR) # store image in IMG_DIR
        print(image_name)
        img_path = IMG_DIR+image_name
        # OCR Stage
        ocr.extract_text(img_path) # TO DO: NEED TO MAKE FUNCTION TO CHECK FOLDER FOR IMAGE NAME
        ocr_df = ocr.text_to_dataframe()

        # NLP Stage
        PHN = nlp.extract_PHN(ocr_df)
        print(PHN)

    #text = ocr.simple_ocr("images/example.png");
    #print("Tesseract OCR output:")
    #print(text)
    #print("Stanford Nlp output:")
    #nlp.simple_nlp(text);

if __name__ == '__main__':
	main()
