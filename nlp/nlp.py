# Simple Example for geting started with tesseract.
# Adapted from the example provided here: https://stanfordnlp.github.io/stanfordnlp/

import stanfordnlp
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')


def extract_PHN(df):
    # Takes pandas dataframe from OCR  and returns extracted PHN
    df_digits_boo = df['text'].str.isdigit()
    # print(df_digits_boo)
    df_mask = df_digits_boo == True
    df_digits = df['text'].loc[df_mask]
    # print(df_digits)
    df_PHN = df_digits.loc[
        df_digits.str.len() >= 8]  # create dataframe of possible PHN (numbers with greater than or equal to 8 digits)
    # print(df_PHN)
    # print('========= END =========')
    return df_PHN.iloc[0]  # Output first in list


def simple_nlp(text):
    stanfordnlp.download('en')
    nlp = stanfordnlp.Pipeline()  # This sets up a default neural pipeline in English
    doc = nlp('David')
    return doc.print_dependencies()


def prepocess_df(dirty_df):
    # drop all rows with text as nan
    clean_df = dirty_df.dropna()

    return clean_df


def hack_extract_names(df):
    # returns list of two consecutive words that have capital first letters
    possible_names = []
    df = prepocess_df(df)

    for i in range(0,df.shape[0]-1):
        if df['text'].iloc[i][0].isupper() and df['text'].iloc[i+1][0].isupper():
            if df['text'].iloc[i][-1] == ",":
                # if format of name is 'Trudeau, Justin'
                if df['text'].iloc[i+1][-1] == ",":
                    possible_names.append(df['text'].iloc[i + 1][:-1] + " " + df['text'].iloc[i])
                else:
                    possible_names.append(df['text'].iloc[i+1][:-1] + " " + df['text'].iloc[i])
            else:
                # if format of name is 'Justin Trudeau'
                if df['text'].iloc[i+1][-1] == ",":
                    possible_names.append(df['text'].iloc[i + 1][:-1] + " " + df['text'].iloc[i])
                else:
                    possible_names.append(df['text'].iloc[i] + " " + df['text'].iloc[i+1])
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

