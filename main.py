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
while True:
    line = sys.stdin.readline()[:-1]
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

