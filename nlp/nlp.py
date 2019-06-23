# NLP module to find patient identifiers from OCR
import nltk
import spacy

# ******* Libraries not in use *************
#import stanfordnlp
#import nltk
#from nltk.corpus import stopwords
#stop = stopwords.words('english')

# INPUT: ocr_df - pandas dataframe of document OCR
# RETURN: possible_names - list of possible names
def extract_PHN(ocr_df):
    # searches OCR dataframe and returns list of PHNs for patient
    possible_PHNs = []

    # create boolean mask for numeric text in ocr_df
    df_digits_boo = ocr_df['text'].str.isdigit()
    df_mask = df_digits_boo == True

    df_digits = ocr_df['text'].loc[df_mask] # create new dataframe of only digits from OCR
    df_PHN = df_digits.loc[df_digits.str.len() >= 8]  # create dataframe of possible PHN (numbers with greater than or equal to 8 digits)
    possible_PHNs = list(df_digits.loc[(df_digits.str.len() > 7) & (df_digits.str.len() < 12)]) # create list of digits that are 7 to 12 characters in length

    return possible_PHNs

# INPUT: ocr_df - pandas dataframe of document OCR
# RETURN: possible_DOBs - list of possible date of births
def extract_DOB(ocr_df): #TODO Need to utilize string OCR not df and develop rules to use with area of interest functions
    # searches OCR dataframe and returns list of possible date of births for patient
    nlp = spacy.load("en_core_web_sm")
    possible_DOBs = []

    for i in range(0, ocr_df.shape[0] - 1):
        word = nlp(ocr_df['text'].iloc[i])
        for ent in word.ents:
            if ent.label_ == 'DATE':
                possible_DOBs.append(ocr_df['text'].iloc[i][0])

    return possible_DOBs


# INPUT: ocr_df - pandas dataframe of document OCR
# RETURN: possible_names - list of possible names
def hack_extract_names(ocr_df):
    # searches OCR dataframe and returns list of names for patient
    # HACK METHOD BECAUSE FUNCTION WILL FAIL IF ALL TEXT ARE UPPERCASE
    possible_names = []

    for i in range(0, ocr_df.shape[0] - 1):
        if ocr_df['text'].iloc[i][0].isupper() and ocr_df['text'].iloc[i + 1][0].isupper():
            if ocr_df['text'].iloc[i][-1] == ",":
                # if format of name is 'Trudeau, Justin'
                if ocr_df['text'].iloc[i + 1][-1] == ",":
                    possible_names.append(ocr_df['text'].iloc[i + 1][:-1] + " " + ocr_df['text'].iloc[i])
                else:
                    possible_names.append(ocr_df['text'].iloc[i + 1][:-1] + " " + ocr_df['text'].iloc[i])
            else:
                # if format of name is 'Justin Trudeau'
                if ocr_df['text'].iloc[i + 1][-1] == ",":
                    possible_names.append(ocr_df['text'].iloc[i + 1][:-1] + " " + ocr_df['text'].iloc[i])
                else:
                    possible_names.append(ocr_df['text'].iloc[i] + " " + ocr_df['text'].iloc[i + 1])
    return possible_names


def pos_tagging(document):
    # Tokenize string  and return array of parts of speech tagging
    sentences = nltk.sent_tokenize(document)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    tagged_words = [nltk.pos_tag(word) for word in words]
    return tagged_words


def extract_names(document):
    # output array of possible  names using NLTK Named Entity Recognition

    names = []
    tagged = pos_tagging(document)
    named_ent = nltk.ne_chunk(tagged[0])
    for chunk in named_ent:
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() == 'PERSON':
                names.append(' '.join([c[0] for c in chunk])) # add possible names to arra
    return names

