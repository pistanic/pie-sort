import preproc # for source see: preproc/
import ocr # for source see: ocr/
import nlp # for source see: nlp/

def main():
	# Preprocessing Stage
	img = preproc.pdftojpg('/home/pie/pie-workspace/PDFs/easytest.pdf', '/home/pie/pie-workspace/images')

	# OCR Stage
	ocr.extract_text('/home/pie/pie-workspace/images/8bb9b56b-20c0-4f56-99dd-f7ebafc689a9-1.ppm') # TO DO: NEED TO MAKE FUNCTION TO CHECK FOLDER FOR IMAGE NAME
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
