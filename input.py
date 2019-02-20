"""
Aux functions to build the index
"""

import re, math

def linguistique_ligne(line, freq, common_words):
    """
    Traitement linguistique pour une ligne
    """
    words = list(filter(None, re.split(r'[^a-z0-9]', line.lower())))
    token = 0
    for word in words:
        token += 1
        if word not in common_words:
            # maj frequence
            try:
                freq[word] += 1
            except KeyError:
                freq[word] = 1
    return token

def traiter_ligne(docID, line, index, freq, common_words, words_set):
    words = list(filter(None, re.split(r'[^a-z0-9]', line.lower())))
    if '' in words:
        print(line)
        print(words)
        # sys.exit()
    token = 0
    for word in words:
        token += 1

        if word not in common_words:

            # maj frequence
            try:
                freq[word] += 1
            except KeyError:
                freq[word] = 1

            # maj indexß
            try:
                if docID in index[word]:
                    index[word][docID] += 1
                else:
                    index[word][docID] = 1
            except KeyError:
                index[word] = {docID: 1}

            # maj word set
            words_set.add(word)
    return token