import ocr # for source see: ocr/
import nlp # for source see: nlp/

def main():
	print("Hello World")
	text = ocr.simple_ocr("images/example.png");
	print("Tesseract OCR output:")
	print(text)
	print("Stanford Nlp output:")
	nlp.simple_nlp(text);

if __name__ == '__main__':
	main()
