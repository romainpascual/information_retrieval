import math, time

"""
Implement vectorial search
"""
def build_vect_space(index:dict, wordDic:dict, collection_size:int):
    modes = ['tf-idf', 'tf-idf-norm', 'freq-norm']
    vect_space = dict()
    for docID in wordDic.values():
        vect_weights = dict()
        for wordID in index.keys():
            mode_weight = dict()
            to_add = False
            for m in modes:
                dtf = get_inverse_document_frequency(wordID, index)
                w = get_word_weight(dtf, collection_size, wordID, docID, index, m)
                if w != 0:
                    to_add = True
                mode_weight[m] = m
            if to_add:
                vect_weights[wordID] = mode_weight
        vect_space[docID] = vect_weights
    return vect_space

def get_term_frequency(wordID: int, document: int, index: dict):
    try:
         return list(j for i, j in index[wordID] if i == document)[0]
    except IndexError:
        return 0

def get_max_term_frequency(document:int, index:dict):
    max_tf = 0
    for docSet in index.values():
        for doc in docSet:
            if doc[0] == document:
                tf = doc[1]
                if tf > max_tf:
                    max_tf = tf
    return max_tf

def get_inverse_document_frequency(wordID: int, index: dict):
    return len(index[wordID])


def get_word_weight(document_frequency: int,
                    collection_size: int,
                    wordID: int,
                    document,
                    index: dict,
                    mode='tf-idf',
                    vectorization='document',
                    tf=None):
    """
    mode = 'tf-idf'
    mode = 'tf-idf-norm'
    mode = 'freq-norm'
    vectorization = 'document' for corpus vectorization
    vectorization = 'query' for query vectorization
    query = query if in query vectorization

    """
    if mode == 'freq-norm' and vectorization == 'query':
        mode = 'tf-idf-norm'

    if vectorization == 'document':
        tf = get_term_frequency(wordID, document, index)
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


def vectorial_search(query: str, collection_size: int, index: dict, wordDic:dict, time_it = False, mode='tf-idf', size=50):
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
    vectorial_query = dict()
    sum_weight2_query = 0
    for word in query.split():
        word = word.lower()
        tf = list(query.split()).count(word)
        if word in wordDic:
            dtf = get_inverse_document_frequency(wordDic[word], index)
            word_weight_query = get_word_weight(dtf,
                                                collection_size,
                                                wordDic[word],
                                                None,
                                                index,
                                                mode=mode,
                                                vectorization='query',
                                                tf=tf)
            sum_weight2_query += word_weight_query**2
        else:
            word_weight_query = 0
        vectorial_query[word] = word_weight_query
    for document in range(collection_size):
        sum_weight_doc_query = 0
        sum_weight2_doc = 0
        for word in query.split():
            word = word.lower()
            if word in wordDic:
                dtf = get_inverse_document_frequency(wordDic[word], index)
                docList = [i for i, _ in index[wordDic[word]]]
                if document in docList:
                    word_weight_document = get_word_weight(dtf, collection_size, wordDic[word], document, index, mode=mode)
                    sum_weight_doc_query += word_weight_document * vectorial_query[word]
                    sum_weight2_doc += word_weight_document**2
        if sum_weight2_doc == 0:
            result[document] = 0
        else:
            result[document] = sum_weight_doc_query / (math.sqrt(sum_weight2_doc)*math.sqrt(sum_weight2_query))
    res = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
    res = [k[0] for k in res[:size] if k[1] > 0]
    if time_it:
        return res, time.time() - timeBeginningRequest
    else:
        return res






