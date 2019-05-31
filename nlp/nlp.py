# Simple Example for geting started with tesseract. 
# Adapted from the example provided here: https://stanfordnlp.github.io/stanfordnlp/

import stanfordnlp

def simple_nlp(text):
	#stanfordnlp.download('en')   # This downloads the English models for the neural pipeline
	nlp = stanfordnlp.Pipeline() # This sets up a default neural pipeline in English
	doc = nlp(text)
	return doc.sentences[0].print_dependencies()

