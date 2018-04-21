

```python
import numpy as np
import pandas as pd
from textblob import TextBlob as tb
from time import time
```

### Creating constants that will be used over this report


```python
COLUMN_AXIS = 1
FULL_REPORT_COLNAME = 'noticia'
CONTENT_COLNAME = 'conteudo'
TITLE_COLNAME = 'titulo'
TOKENS_COLNAME = 'tokens'
TERM_COLNAME = 'term'
REPORT_ID_COLNAME = 'idNoticia'
AND = 'AND'
OR = 'OR'
```

# Meeting data


```python
df = pd.read_csv('../data/noticias_estadao.csv')
```


```python
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>titulo</th>
      <th>conteudo</th>
      <th>idNoticia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>11 dos eleitores do País são filiados a legendas</td>
      <td>Há porém variações regionais nesse fenômeno En...</td>
      <td>7617</td>
    </tr>
    <tr>
      <th>1</th>
      <td>11 executivos integram 1º pedido de condenação...</td>
      <td>CURITIBA A força-tarefa da Operação Lava Jato ...</td>
      <td>412</td>
    </tr>
    <tr>
      <th>2</th>
      <td>11 executivos integram 1º pedido de condenação...</td>
      <td>CURITIBA A força-tarefa da Operação Lava Jato ...</td>
      <td>415</td>
    </tr>
    <tr>
      <th>3</th>
      <td>13 de deputados do PMDB quer romper com PT</td>
      <td>O Estado ouviu 54 dos 74 deputados do PMDB em ...</td>
      <td>6736</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2014 começou em 2007</td>
      <td>O estudo do Estadão Dados publicado ontem sobr...</td>
      <td>7611</td>
    </tr>
  </tbody>
</table>
</div>




```python
print("Data has %d rows and %d columns" % df.shape)
```

    Data has 7643 rows and 3 columns


# Concatenatin galls reports' title and content in just one column.


```python
def concatenate_report(row):
    """Concatenate report title and content in just one column.
        
    Args:
        row (:obj: pandas.Series): one row observation from a pandas.DataFrame.            

    Return:
        str: full report (content with title) in lowercase.
    """

    full_report = row[TITLE_COLNAME] + " " + row[CONTENT_COLNAME]
    return full_report.lower()
```


```python
df[FULL_REPORT_COLNAME] = df.apply(
    lambda row: concatenate_report(row), axis=COLUMN_AXIS)
```

Selecting just report's id and full content columns:


```python
df = df[[REPORT_ID_COLNAME, FULL_REPORT_COLNAME]]
```

Dataframe now looks like:


```python
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>idNoticia</th>
      <th>noticia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7617</td>
      <td>11 dos eleitores do país são filiados a legend...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>412</td>
      <td>11 executivos integram 1º pedido de condenação...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>415</td>
      <td>11 executivos integram 1º pedido de condenação...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6736</td>
      <td>13 de deputados do pmdb quer romper com pt o e...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7611</td>
      <td>2014 começou em 2007 o estudo do estadão dados...</td>
    </tr>
  </tbody>
</table>
</div>



# Tokenizing report's text and saving tokens in another column in dataframe


```python
def tokenize_text(row):
    """Tokenize the text content of a report given as a row from a DataFrame
        
    Args:
        row (:obj: pandas.Series): one row observation from a pandas.DataFrame.            

    Return:
        set: a report content turned into a set of tokens.
    """    
    
    text_blob = tb(row[FULL_REPORT_COLNAME]) 
    m_tokens = set(text_blob.words)
    return m_tokens
```


```python
df[TOKENS_COLNAME] = df.apply(
    lambda row: tokenize_text(row), axis=COLUMN_AXIS)
```

# Creating inverted index

First, we will create a intermediate structure called unnested_tokens. This structure will save each token of a report individually, associating it to the report's id. After this step, we will group this unnested_tokens structure by tokens, getting all reports' ids where one specific token appears.


```python
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
```


```python
unnested_tokens_list = []
df.apply(lambda row: unnest_tokens_report(unnested_tokens_list, row), axis=COLUMN_AXIS)

print("\nThe unnested_tokens_list looks like: \n")
print(unnested_tokens_list[:8])
print("\nThe 'list of dicts' format will be used to create a pandas.DataFrame:")
```

    
    The unnested_tokens_list looks like: 
    
    [{'term': 'possa', 'idNoticia': 7617}, {'term': 'das', 'idNoticia': 7617}, {'term': 'lançamento', 'idNoticia': 7617}, {'term': 'foram', 'idNoticia': 7617}, {'term': 'impacta', 'idNoticia': 7617}, {'term': 'busca', 'idNoticia': 7617}, {'term': '81', 'idNoticia': 7617}, {'term': 'dinâmica', 'idNoticia': 7617}]
    
    The 'list of dicts' format will be used to create a pandas.DataFrame:



```python
unnested_tokens_df = pd.DataFrame(unnested_tokens_list)
unnested_tokens_df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>idNoticia</th>
      <th>term</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7617</td>
      <td>possa</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7617</td>
      <td>das</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7617</td>
      <td>lançamento</td>
    </tr>
    <tr>
      <th>3</th>
      <td>7617</td>
      <td>foram</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7617</td>
      <td>impacta</td>
    </tr>
    <tr>
      <th>5</th>
      <td>7617</td>
      <td>busca</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7617</td>
      <td>81</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7617</td>
      <td>dinâmica</td>
    </tr>
    <tr>
      <th>8</th>
      <td>7617</td>
      <td>intrapartidária</td>
    </tr>
    <tr>
      <th>9</th>
      <td>7617</td>
      <td>fez</td>
    </tr>
  </tbody>
</table>
</div>



### Grouping by term to create inverted index


```python
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
```


```python
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
```

Creating the inverted index structure for our data:


```python
m_inverted_index = create_inverted_index_structure(unnested_tokens_df)
```

## Processing Queries


```python
def is_one_term_query(query):
    
    empty_str, space_str = "", " "    
    
    if query == empty_str or query == space_str:
        raise ValueError('You should search for a non empty string.')        
    else:
        return len(query.split(space_str)) == 1
```


```python
def get_query_operator(query):    
    """Get boolean query operator.
    
    Args:
        query (str): query with more than one term.
    
    Return:
        str: string name for the boolean query operator.
    """  
    
    if AND not in query and OR not in query:
        raise ValueError('Thats not a valid query.')  
    
    return AND if AND in query else OR
```


```python
def lowercase_iterable_itens(iterable):
    """Lowercase all itens in a iterable object.
    
    Args:
        iterable (list): list of str itens to lowercase.
    
    Return:
        list: list with elements in lowercase.
    """      
    return list(map(lambda term: term.lower(), iterable))
```


```python
def _intersect(list1, list2):
    """Found all elements that are commom to two lists."""           
    
    result = []    
    i, j = 0, 0    
    
    while i < len(list1) and j < len(list2):    
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1        
        else:            
            if list1[i] < list2[j]:
                i += 1
            else:
                j += 1
    
    return result
```


```python
def _union(list1, list2):
    """Found the union (with no repetition) of elements of two given lists."""           
    
    result = []    
    i, j = 0, 0
    
    while i < len(list1) and j < len(list2):    
        if list1[i] < list2[j]:
            result.append(list1[i])
            i += 1      
        elif list1[i] > list2[j]:            
            result.append(list2[j])
            j += 1 
        else:
            result.append(list1[i])
            i += 1
            j += 1

    while i < len(list1):    
        result.append(list1[i])
        i += 1      
    
    while j < len(list2):    
        result.append(list2[j])
        j += 1      
            
    return result
```


```python
def sort_terms_list_per_freq(terms_list, inverted_index):
    """Sort list of terms to search by their frequency. Frequency of a term can be found in the InvertedIndexTerm
    object saved in the inverted index structure to the corresponding key term.
    
    Args:
        terms_list (list): list to sort.
        inverted_index (dict): structure through which get term's frequency.
    
    Return:
        list: sorted list of InvertedIndexTerm objects.
    """      
    terms_obj_list = list(map(lambda term: inverted_index[term], terms_list))    
    terms_obj_list.sort(key= lambda term: term.get_freq())
    return terms_obj_list
```


```python
def _boolean_search(terms_to_search, operator, inverted_index):
      
    sorted_terms_per_freq = sort_terms_list_per_freq(terms_to_search, inverted_index)
    
    docs_ids = sorted_terms_per_freq[0].get_docs_ids()   
    result = docs_ids
    
    for another_term in sorted_terms_per_freq:
        
        docs_ids = another_term.get_docs_ids()  
    
        if operator == AND:
            result = _intersect(result, docs_ids)
        elif operator == OR:
            result = _union(result, docs_ids)
            
    return list(result)
```


```python
def search(query, inverted_index):
    
    if is_one_term_query(query):
        term = query.lower()
        return inverted_index[term].get_docs_ids()  
    
    else:    
        operator = get_query_operator(query)
        terms_to_search = query.split(" " + operator + " ")
        terms_to_search = lowercase_iterable_itens(terms_to_search)
        
        return _boolean_search(terms_to_search, operator, inverted_index)
```

# Sanities checks


```python
search_result = sorted(search("Campina AND Grande", m_inverted_index))
correct_answer = sorted([1952, 4802, 1987, 6694, 5382, 1770, 2763, 1068, 5870, 2777, 1370, 2779])
assert search_result == correct_answer
```

# Tests

### 1. debate, presidenciável (AND e OR)


```python
assert len(search("debate OR presidencial", m_inverted_index)) == 1770
assert len(search("debate AND presidencial", m_inverted_index)) == 201
```

### 2. presidenciáveis, corruptos (AND e OR)


```python
assert len(search("presidenciáveis OR corruptos", m_inverted_index)) == 164
assert len(search("presidenciáveis AND corruptos", m_inverted_index)) == 0
```

### 3. Belo, Horizonte (AND e OR)


```python
assert len(search("Belo OR Horizonte", m_inverted_index)) == 331
assert len(search("Belo AND Horizonte", m_inverted_index)) == 242
```

### 4. candidatos (one term query)


```python
msg_out = "Searching for word 'candidatos' results in %d reports containing this word."
n_reports = len(search("candidatos", m_inverted_index))
print(msg_out % n_reports)
```

    Searching for word 'candidatos' results in 1395 reports containing this word.


# Bonus


```python
assert len(search("PT AND Golpe AND Inflação", m_inverted_index)) <= min(len(search("PT", m_inverted_index)), len(search("Golpe", m_inverted_index)), len(search("Inflação", m_inverted_index)))
```
