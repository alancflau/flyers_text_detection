import pandas as pd
import numpy as np
import re
from ftfy import fix_text

from sklearn.feature_extraction.text import TfidfVectorizer
import time
import nmslib

def ngrams(text, n = 3):
    """
    :param text:
    :param n: n is set to default of 3
    :return: ngrams
    """
    # Specific case to replace/modify?

    string = str(text)
    string = string.lower() # lower case
    string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode()
    chars_to_remove = [")","(",".","|","[","]","{","}","'","-"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']' #remove punc, brackets etc...
    string = re.sub(rx, '', string)
    string = string.title()
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def create_ref_tfidf_matrix(dataframe):

    t1 = time.time() #start time
    prod_items_reference = list(dataframe['input1_column'].unique()) # unique product flyer names

    # Build TFIDF off clean dataset
    vectorizer = TfidfVectorizer(min_df = 1, analyzer = ngrams)
    tf_idf_matrix = vectorizer.fit_transform(prod_items_reference)
    t = time.time() - t1
    return tf_idf_matrix

def create_messy_tfidf_matrix(dataframe,vectorizer):
    messy_names = list(dataframe['input2_column'].unique())  # unique list of names
    # from create_ref_tfidf_matrix
    messy_tf_idf_matrix = vectorizer.transform(messy_names)


def set_indices(df1, df2):
    pass

