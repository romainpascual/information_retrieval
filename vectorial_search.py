import math, time

"""
Implement vectorial search
"""


def get_term_frequency(word: str, document: int, index: dict, wordDic:dict):
    try:
         return list(j for i, j in index[wordDic[word]] if i == document)[0]
    except IndexError:
        return 0

def get_max_term_frequency(document:int, index:dict):
    max_tf = 0
    for docSet in index.values():
        if docSet[0] == document:
            tf = docSet[1]
            if tf > max_tf:
                max_tf = tf
    return max_tf

def get_inverse_document_frequency(word: str, index: dict, wordDic:dict):
    return len(index[wordDic[word]])


def get_word_weight(document_frequency: int, collection_size: int, word:str, document:int , index: dict, wordDic:dict, mode='tf-idf'):
    """
    mode = 'tf-idf'
    mode = 'tf-idf-norm'
    mode = 'freq-norm'
    """
    tf = get_term_frequency(word, document, index, wordDic)
    idf = math.log(collection_size / document_frequency, 10)

    if mode == 'tf-idf':
        # w(t,d) = tf * idf
        return tf * idf
    elif mode == 'tf-idf-norm':
        # w(t,d) = (1+log(tf)) * idf
        return (1+math.log(tf, 10))*idf
    elif mode == 'freq-norm':
        # w(t_i,d) = tf(t_i,d)/ max_{t_j \in d} tf(t_j,d)
        max_tf = get_max_term_frequency(document, index)
        if max_tf == 0:
            return 0
        return tf / max_tf


def vectorial_search(query: str, collection_size: int, index: dict, wordDic:dict, time_it = False, mode='tf-idf'):
    """
    Vectorial search algorithm implementation.
    :param query: list of K query terms
    :param collection_size: number of documents in the collection
    :param index: inverted index of the collection
    :param wordDic: word to wordID dictionnary
    :param mode: search mode. 'tf-idf', 'normalized-tf-idf', 'normalized-frequency'
    :return:
    """
    
    timeBeginningRequest = time.time()
    result = dict()
    for document in range(collection_size):
        sum_weight_doc = 0
        sum_weight2_doc = 0
        for word in query.split():
            dtf = get_inverse_document_frequency(word, index, wordDic)
            if document in [i for i, _ in index[wordDic[word]]]:
                word_weight = get_word_weight(dtf, collection_size, word, document, index, wordDic)
                sum_weight_doc += word_weight
                sum_weight2_doc += word_weight**2
        if sum_weight2_doc == 0:
            result[document] = 0
        else:
            result[document] = sum_weight_doc / math.sqrt(sum_weight2_doc)
    res = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
    res = [k[0] for k in res]
    if time_it:
        return res, time.time() - timeBeginningRequest
    else:
        return res






