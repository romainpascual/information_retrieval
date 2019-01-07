import math


def get_term_frequency(word: str, document: int, index: dict):
    try:
        return list(j for i, j in index[word] if i == document)[0]
    except IndexError:
        return 0


def get_inverse_document_frequency(word: str, index: dict):
    return len(index[word])


def get_word_weight(term_frequency: int, document_frequency: int, collection_size: int, mode='tf-idf'):
    if mode == 'tf-idf':
        return (1+math.log(term_frequency, 10))*math.log(collection_size / document_frequency, 10)


def vectorial_search(query: list, collection_size: int, index: dict, mode='tf-idf'):
    """
    Vectorial search algorithm implementation.
    :param query: list of K query terms
    :param collection_size: number of documents in the collection
    :param index: inverted index of the collection
    :param mode: search mode. 'tf-idf', 'normalized-tf-idf', 'normalized-frequency'
    :return:
    """

    result = dict()
    for document in range(collection_size):
        sum_weight_doc = 0
        sum_weight2_doc = 0
        for word in query:
            dtf = get_inverse_document_frequency(word, index)
            if document in [i for i, _ in index[word]]:
                tf = get_term_frequency(word, document, index)
                word_weight = get_word_weight(tf, dtf, collection_size)
                sum_weight_doc += word_weight
                sum_weight2_doc += word_weight**2
        if sum_weight2_doc == 0:
            result[document] = 0
        else:
            result[document] = sum_weight_doc / math.sqrt(sum_weight2_doc)

    return sorted(result.items(), key=lambda kv: kv[1], reverse=True)






