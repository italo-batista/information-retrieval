import nltk
import pandas as pd
import re

def remove_punctuation(word):
    return re.sub('[,.]', '', word)

def clean_special_chars(special_chars, list_to_clean):
    return list(filter(lambda item: item not in special_chars, list_to_clean))

def tokenize_text(row, text_colname):
    """Tokenize the text content of a report given as a row from a DataFrame
        
    Args:
        row (:obj: pandas.Series): one row observation from a pandas.DataFrame.
        text_colname (str): name of column df whose rows will be tokenized.

    Return:
        set: a report content turned into a set of tokens.
    """    
    special_chars = [',', '.', '"', '”', '-', '_', '$', '“']
    m_tokens = nltk.word_tokenize(row[text_colname])
    m_tokens = clean_special_chars(special_chars, m_tokens)
    m_tokens = list(map(remove_punctuation, m_tokens))
    return m_tokens

def tokenize(df, text_colname, new_tokens_colname):
    """Tokenize the text content of an given df in a specific column. Save tokens
    in a new column.
        
    Args:
        text_colname (str): name of column df whose rows will be tokenized.
        new_tokens_colname (str): name column that will be created to save tokens.

    Return:
        :obj: DataFrame: df modified with column of tokens.
    """ 
    COLUMN_AXIS = 1
    df[new_tokens_colname] = df.apply(
        lambda row: tokenize_text(row, text_colname), axis=COLUMN_AXIS)
    return df