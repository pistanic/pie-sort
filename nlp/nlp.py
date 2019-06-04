# Simple Example for geting started with tesseract.
# Adapted from the example provided here: https://stanfordnlp.github.io/stanfordnlp/

import stanfordnlp


def extract_PHN(df):
    # Takes pandas dataframe from OCR  and returns extracted PHN
    df_digits_boo = df['text'].str.isdigit()
    df_mask = df_digits_boo == True
    df_digits = df['text'].loc[df_mask]
    df_PHN = df_digits.loc[df_digits.str.len()>5] # create dataframe of possible PHN (numbers with greater than 5 digits)
    return df_PHN.iloc[0] # Output first in list

def simple_nlp(text):
	#stanfordnlp.download('en')   # This downloads the English models for the neural pipeline
	nlp = stanfordnlp.Pipeline() # This sets up a default neural pipeline in English
	doc = nlp(text)
	return doc.sentences[0].print_dependencies()
