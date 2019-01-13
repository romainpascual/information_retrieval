import time

### Modèle de recherche booléen
"""
Using infix form allow us not to use parenthesis

What do to when we read something in the request?
    - word => get posting
    - NOT => get the complementary of the recursive call result
    - AND => get the intersection of the two next recursive call results
    - OR => get the union of the two next recursive call results

example:
AND teletype OR console debugging
"""

class NotExpr(Exception):pass

def get_complementary_posting(posting, collection_size):
    return set(range(1,collection_size+1)).difference(posting)

def get_posting(word, index):
    try:
        return set(dicoDoc[0] for dicoDoc in index[word])
    except KeyError:
        return set()

def analyse_expr(request, index, collection_size):
    current = request.pop(0)

    # NOT
    if current == 'NOT':
        # right after the negation is a word
        nextword = request.pop(0).lower()
        # we build the posting of this word
        posting = get_posting(nextword, index)
        # return the complement
        return get_complementary_posting(posting, collection_size)

    # OR
    elif current == 'OR':
        # deal with the first expression
        first = analyse_expr(request, index, collection_size)
        # deal with the second expression
        second = analyse_expr(request, index, collection_size)
        # return the union of the postings
        return first.union(second)

    # AND
    elif current == 'AND':
        # deal with the first expression
        first = analyse_expr(request, index, collection_size)
        # deal with the second expression
        second = analyse_expr(request, index, collection_size)
        # return the intersection of the expression
        return first.intersection(second)

    # it's a word
    else:
        return get_posting(current.lower(), index)

def boolean_search(query: str, collection_size: int, index: dict, time_it=False):
    """
    Boolean search algorithm implementation.
    :param query: boolean expression describing the query
    :param collection_size: number of documents in the collection
    :param index: inverted index of the collection
    :param time_it: boolean to enable performance measures
    :return:
    """

    request = query.split()

    if time_it:
       timeBeginningRequest = time.time()
    
    res = sorted(list(analyse_expr(request, index, collection_size)))
    
    timeEndRequest = time.time()

    return res if (not time_it) else res, timeEndRequest - timeBeginningRequest