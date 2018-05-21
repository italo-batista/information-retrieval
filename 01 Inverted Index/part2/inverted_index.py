import numpy as np
import pandas as pd
import collections
import nltk
from time import time
from abc import ABC, abstractmethod
import re

COLUMN_AXIS = 1
TERM_COLNAME = 'term'
TOKENS_COLNAME = 'tokens'
REPORT_ID_COLNAME = 'idNoticia'

class InvertedIndexTerm:
    """Class for register term frequency and docs' ids in which a 
    term of a inverted index structure appears.
    
    Attributes:
        term_freq (int): Quantity of docs in which term appears.
        docs_ids (list): ids of docs in which term appears.
    """
    
    def __init__(self, term, freq, docs_ids):
        self.term = term
        self.freq = freq
        self.docs_ids = sorted(list(docs_ids))
    
    def get_term(self):
        return self.term
    
    def get_freq(self):
        return self.freq
    
    def get_docs_ids(self):
        return self.docs_ids

def unnest_tokens_report(unnested_tokens_list, row):
    """Given a row observation of a DataFrame to represent a report (with content,
    tokens and id), iterate over the set of tokens and save each one as a dict with 
    token value and report id. Each dict is appended in the unnested_tokens_list
    passed as param.
        
    Args:
        unnested_tokens_list (list): list of dicts, each dict containing a token value 
            and the report id where it occured.
        row (:obj: pandas.Series): one row observation from a pandas.DataFrame.            
    """  
        
    for token in row[TOKENS_COLNAME]:
        new_row = {
            TERM_COLNAME: token.strip('\'').strip(),
            REPORT_ID_COLNAME: row[REPORT_ID_COLNAME]}
        unnested_tokens_list.append(new_row)    
           
def create_inverted_index_structure(unnested_tokens_df):
    """Create a inverted index structure using python dict structure.
    
    Args:
        unnested_tokens_df (:obj: pandas.DataFrame): unnested tokens of texts from a set of texts.
    
    Return:
        dict: keys are terms found at texts and values are lists of docs_ids where terms are found.
    """    
    inverted_index = dict()

    for term, group_itens in unnested_tokens_df.groupby([TERM_COLNAME]):

        term_freq = len(group_itens.get_values())
        docs_ids = set(group_itens[REPORT_ID_COLNAME])
        inverted_index[term] = InvertedIndexTerm(term, term_freq, docs_ids)
    
    return inverted_index    

def get_inverted_index(df):
    """First, we will create a intermediate structure called unnested_tokens. This structure will save each 
    token of a report individually, associating it to the report's id. After this step, we will group this 
    unnested_tokens structure by tokens, getting all reports' ids where one specific token appears."""
    
    unnested_tokens_list = []
    df.apply(lambda row: unnest_tokens_report(unnested_tokens_list, row), axis=COLUMN_AXIS)
    unnested_tokens_df = pd.DataFrame(unnested_tokens_list)   
    inverted_index = create_inverted_index_structure(unnested_tokens_df)
    return inverted_index

