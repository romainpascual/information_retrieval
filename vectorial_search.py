import math, time

"""
Implement vectorial search
"""


def get_term_frequency(word: str, document: int, index: dict, wordDic:dict):
    try:
        return list(j for i, j in index[wordDic[word]] if i == document)
    except IndexError:
        return 0


def get_inverse_document_frequency(word: str, index: dict, wordDic:dict):
    return len(index[wordDic[word]])


def get_word_weight(term_frequency: int, document_frequency: int, collection_size: int, mode='tf-idf'):
    if mode == 'tf-idf':
        return (1+math.log(term_frequency, 10))*math.log(collection_size / document_frequency, 10)


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

    if time_it:
       timeBeginningRequest = time.time()
    result = dict()
    for document in range(collection_size):
        sum_weight_doc = 0
        sum_weight2_doc = 0
        for word in query.split():
            dtf = get_inverse_document_frequency(word, index, wordDic)
            if document in [i for i, _ in index[wordDic[word]]]:
                tf = get_term_frequency(word, document, index, wordDic)
                word_weight = get_word_weight(tf, dtf, collection_size)
                sum_weight_doc += word_weight
                sum_weight2_doc += word_weight**2
        if sum_weight2_doc == 0:
            result[document] = 0
        else:
            result[document] = sum_weight_doc / math.sqrt(sum_weight2_doc)
    timeEndRequest = time.time()
    res = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
    return res if (not time_it) else res, timeEndRequest - timeBeginningRequest






