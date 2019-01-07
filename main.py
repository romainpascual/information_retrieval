import sys
import re
import math
from matplotlib import pyplot as plt
import scipy.stats

index = dict()
common_words = set()
freq = dict()

token = 0


logT = []
logM = []

with open("data/CACM/common_words", "r") as common_words_list:
    for word in common_words_list:
        common_words.add(word[:-1])


def traiter_ligne(docID, line):
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
    return token

reading = False
with open("data/CACM/cacm.all", "r") as cacm:
    while True:
        line = cacm.readline()[:-1]
        if not line:
            break
        if line[0:2] == ".I":
            docID = int(line.split(' ')[1])
        if line[0:2] in [".T", ".W", ".K"]:
            reading = True
        elif line[0] == ".":
            reading = False
        elif reading:
            token += traiter_ligne(docID, line)
            logT.append(math.log(token, 10))
            logM.append(math.log(len(index), 10))

# On obtient un index de la forme {mot: [(docId1, frequency1), (docId2, frequency2), ...]}
# Cela répond à la question 2.2 pour cacm
for word, dicoDoc in index.items():
    index[word] = [(docID, frequency) for docID, frequency in dicoDoc.items()]
    index[word].sort()

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(logT[len(logT)//2:], logM[len(logM)//2:])

b = slope
k = 10**intercept
print("Il y a {} tokens dans la collection.".format(token))
print("Il y a {} mots dans le vocabulaire.".format(len(index)))
print("b: ", b)
print("log(k): ", intercept)
print('k: ', k)
print("Pour 1 000 000 de tokens, il y aurait {} mots de vocabulaire.".format(int(k*10e6**b)))
# plt.plot(logT, logM)
# plt.show()

# for word, docIDs in index.items():
#     print(type(docIDs))
#     break

rang = []
for word in index.keys():
    rang.append((word, sum(value[1] for value in index[word])))
rang.sort(key=lambda x : x[1], reverse=True)
#print(rang)

rangFreq = [rg[1] for rg in rang]

plt.plot(range(1, len(rang)+1),rangFreq)
plt.savefig("freq_vs_rg.png")
#plt.show()

logRang=[math.log10(k) for k in range(1, len(rang)+1)]
logFreq=[math.log10(f) for f in rangFreq]

plt.plot(logRang, logFreq)
plt.savefig("logFreq_vs_logRg.png")
#plt.show()


## NB remplacer par rang.append(sum(value[1] for value in index[word])) lorsque la lecture est corrigée.



### Modèle de recherche booléen
"""
On utilise la forme infixe. On a donc pas besoin de parenthese

word -> on cherche le posting
NOT -> on prend le complément de ce qui est retrourné par l'appel récursif
AND -> on prend l'intersection des deux appels récursifs
OR -> on prend l'union des deux appels récursifs

exemple:
AND teletype OR console debugging
"""

class NotExpr(Exception):pass
allDocIDs = set(range(1,docID+1))

def get_posting(word):
    try:
        return set(dicoDoc[0] for dicoDoc in index[word])
    except KeyError:
        return set()

def analyse_expr(lst):
    current = lst.pop(0)

    # NOT
    if current == 'NOT':
        # right after the negation is a word
        nextword = lst.pop(0).lower()
        # we build the posting of this word
        posting = get_posting(nextword)
        # return the complement
        return allDocIDs.difference(posting)
    
    # OR
    elif current == 'OR':
        # deal with the first expression
        first = analyse_expr(lst)
        # deal with the second expression
        second = analyse_expr(lst)
        # return the union of the postings
        return first.union(second)
    
    # AND
    elif current == 'AND':
        # deal with the first expression
        first = analyse_expr(lst)
        # deal with the second expression
        second = analyse_expr(lst)
        # return the intersection of the expression
        return first.intersection(second)

    # it's a word
    else:
        return get_posting(current.lower())

doARequest = 1

while(doARequest):
    try:
        doARequest = int(input("Do you want to do a boolean request ?[0/1]\n"))
    except ValueError:
        break
    if doARequest == 1:
        print(analyse_expr(input("Please enter your request using infix from.\n").split()))


