
def is_one_term_query(query):
    
    empty_str, space_str = "", " "    
    
    if query == empty_str or query == space_str:
        raise ValueError('You should search for a non empty string.')        
    else:
        return len(query.split(space_str)) == 1
    
def get_query_operator(query):    
    """Get boolean query operator.
    
    Args:
        query (str): query with more than one term.
    
    Return:
        str: string name for the boolean query operator.
    """  
    
    if 'AND' not in query and 'OR' not in query:
        raise ValueError('Thats not a valid query.')  
    
    return 'AND' if 'AND' in query else 'OR'   

def lowercase_iterable_itens(iterable):
    """Lowercase all itens in a iterable object.
    
    Args:
        iterable (list): list of str itens to lowercase.
    
    Return:
        list: list with elements in lowercase.
    """      
    return list(map(lambda term: term.lower(), iterable))

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

def _boolean_search(terms_to_search, operator, inverted_index):
      
    sorted_terms_per_freq = sort_terms_list_per_freq(terms_to_search, inverted_index)
    
    docs_ids = sorted_terms_per_freq[0].get_docs_ids()   
    result = docs_ids
    
    for another_term in sorted_terms_per_freq:
        
        docs_ids = another_term.get_docs_ids()  
    
        if operator == 'AND':
            result = _intersect(result, docs_ids)
        elif operator == 'OR':
            result = _union(result, docs_ids)
            
    return list(set(result))

def search(query, inverted_index):
    
    if is_one_term_query(query):
        term = query.lower()
        return inverted_index[term].get_docs_ids()  
    
    else:    
        operator = get_query_operator(query)
        terms_to_search = query.split(" " + operator + " ")
        terms_to_search = lowercase_iterable_itens(terms_to_search)
        
        return _boolean_search(terms_to_search, operator, inverted_index)
    