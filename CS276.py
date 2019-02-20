import sys
import re
import math
from matplotlib import pyplot as plt
import scipy.stats
import time
import os
from tqdm import tqdm
import pickle

from input import traiter_ligne, linguistique_ligne

# Traitements linguistiques
common_words = set()
freq = dict()
words = set()
token = 0
logT = []
logM = []
for folder in range(10):
    print("Traitements linguistiques sur la collection CS276/{}.".format(folder))

    for docID, filename in enumerate(tqdm(os.listdir('data/CS276/'+str(folder)),desc="Index {}".format(folder))):
        with open('data/CS276/'+str(folder)+'/'+filename, "r") as file:
            line = file.readline()
            token += linguistique_ligne(line, freq, common_words, words, logT, logM)

print(words)

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(logT[len(logT)//2:], logM[len(logM)//2:])

b = slope
k = 10**intercept
print("Il y a {} tokens dans la collection.".format(token))
print("Il y a {} mots dans le vocabulaire.".format(len(words)))
print("b: ", b)
print("log(k): ", intercept)
print('k: ', k)
print("Pour 1 000 000 de tokens, il y aurait {} mots de vocabulaire.".format(int(k*10e6**b)))
plt.plot(logT, logM)
plt.show()

exit()

# Indexation
def save_index(index, name):
    with open('indexes/' + name + '.index', 'wb+') as f:
        pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)


for folder in range(10):
    print("Création de l'index sur la collection CS276/{}.".format(folder))
    timeBeginningIndexCreation = time.time()
    index = dict()
    common_words = set()
    freq = dict()
    token = 0
    logT = []
    logM = []
    for docID, filename in enumerate(tqdm(os.listdir('data/CS276/'+str(folder)),desc="Index {}".format(folder))):
        with open('data/CS276/'+str(folder)+'/'+filename, "r") as file:
            line = file.readline()
            token += traiter_ligne(docID, line, index, freq, common_words)
            logT.append(math.log(token, 10))
            logM.append(math.log(len(index), 10))

    # Nombre de documents dans la collection
    collection_doc_nb = docID+1
    # On obtient un index de la forme {mot: [(docId1, frequency1), (docId2, frequency2), ...]}
    # Cela répond à la question 2.2 pour cacm
    for word, dicoDoc in index.items():
        index[word] = [(docID, frequency) for docID, frequency in dicoDoc.items()]
        index[word].sort()

    timeEndIndexCreation = time.time()

    print("Il a fallu {:.4f}s pour créer l'index {}.".format(timeEndIndexCreation - timeBeginningIndexCreation, folder))
    print("Enregistrement de l'index {0} dans 'indexes/CS276_{0}.index'".format(folder))
    save_index(index, "CS276_{}".format(folder))
    print("-"*12)

#
# # for word, docIDs in index.items():
# #     print(type(docIDs))
# #     break
#
# rang = []
# for word in index.keys():
#     rang.append((word, sum(value[1] for value in index[word])))
# rang.sort(key=lambda x : x[1], reverse=True)
# #print(rang)
#
# rangFreq = [rg[1] for rg in rang]
#
# plt.plot(range(1, len(rang)+1),rangFreq)
# plt.savefig("freq_vs_rg.png")
# #plt.show()
#
# logRang=[math.log10(k) for k in range(1, len(rang)+1)]
# logFreq=[math.log10(f) for f in rangFreq]
#
# plt.plot(logRang, logFreq)
# plt.savefig("logFreq_vs_logRg.png")
# plt.show()
#
#
# ## NB remplacer par rang.append(sum(value[1] for value in index[word])) lorsque la lecture est corrigée.
#
# # requests
#
# import boolean_search
# doBooleanRequest = 1
# while(doBooleanRequest):
#     try:
#         doBooleanRequest = int(input("Do you want to do a boolean request ?[0/1]\n"))
#         time_it = int(input("Do you want to time it ?"))
#     except ValueError:
#         break
#     if doBooleanRequest == 1:
#         query = input("Please enter your request using infix form.\n")
#         if time_it:
#             res, qtime = boolean_search.boolean_search(query, collection_doc_nb, index, time_it)
#             print("Cela correspond aux documents :",res)
#             print("Requete exécutée en {:.4f}s.".format(qtime))
#         else:
#             res =  boolean_search.boolean_search(query, collection_doc_nb, index, time_it)
#             print("Cela correspond aux documents :",res)
#
# import vectorial_search
# doVectorialRequest = 1
# while(doVectorialRequest):
#     try:
#         doVectorialRequest = int(input("Do you want to do a vectorial request ?[0/1]\n"))
#         time_it = int(input("Do you want to time it ?"))
#     except ValueError:
#         break
#     if doBooleanRequest == 1:
#         query = input("Please enter your request as the words to search.\n")
#         if time_it:
#             res, qtime = vectorial_search.vectorial_search(query,collection_doc_nb,index, time_it)
#             print("Cela correspond aux documents :",res)
#             print("Requete exécutée en {:.4f}s.".format(qtime))
#         else:
#             res =  vectorial_search.vectorial_search(query, collection_doc_nb, index, time_it)
#             print("Cela correspond aux documents :",res)
 