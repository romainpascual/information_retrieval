"""
Fonctions auxiliaires pour le traitement des données
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

def index_ligne(docID, line, index, wordDic, wordID, common_words):
    """
    Traitement d'une ligne pour la construction de l'index
    """
    words = list(filter(None, re.split(r'[^a-z0-9]', line.lower())))
    for word in words:
        if word not in common_words:

            # maj words
            if word not in wordDic:
                wordDic[word] = wordID
                wordID += 1
        
            # maj indexß
            w_ID = wordDic[word]
            try:
                if docID in index[w_ID]:
                    index[w_ID][docID] += 1
                else:
                    index[w_ID][docID] = 1
            except KeyError:
                index[w_ID] = {docID:1}
    
    return wordID

def vbe_index_ligne(docID, line, index, wordDic, wordID):
    """
    Traitement d'une ligne pour la construction de l'index avec la compression Variable Byte Encoding
    """
    words = list(filter(None, re.split(r'[^a-z0-9]', line.lower())))
    for word in words:
        # maj words
        if word not in wordDic:
            wordDic[word] = wordID
            wordID += 1
    
        # maj indexß
        w_ID = wordDic[word]
        try:
            index[w_ID].add(docID)
        except KeyError:
                index[w_ID] = set([docID])
    
    return wordID