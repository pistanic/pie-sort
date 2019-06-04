import preproc # for source see: preproc/
import ocr # for source see: ocr/
import nlp # for source see: nlp/

def main():
    # Preprocessing Stage
    img = preproc.pdftojpg('./PDF/1.pdf', './tmp/images/')

    filename = '94552282-22a4-45a8-a1ec-d90bd5e39f25-1.ppm'
    # OCR Stage
    ocr.extract_text('./tmp/images/'+filename) # TO DO: NEED TO MAKE FUNCTION TO CHECK FOLDER FOR IMAGE NAME
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
