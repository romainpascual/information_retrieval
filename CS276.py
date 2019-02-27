import sys
import re
import math
from matplotlib import pyplot as plt
import scipy.stats
import time
import os
from tqdm import tqdm
import pickle

# --------------------------------------
# -- Traitement linguistique
# --------------------------------------
doLanguageProcessing = 0
try:
    doLanguageProcessing = int(input("Do you want to do language processing ?[0/1]\n"))
except ValueError:
    pass
if doLanguageProcessing == 1:
    from input import linguistique_ligne

    common_words = set()
    freq = dict()
    token = 0
    logT = []
    logM = []
    for folder in range(10):
        print("Traitements linguistiques sur la collection CS276/{}.".format(folder))

        for docID, filename in enumerate(tqdm(os.listdir('data/CS276/'+str(folder)),desc="Index {}".format(folder))):
            with open('data/CS276/'+str(folder)+'/'+filename, "r") as file:
                line = file.readline()
                token += linguistique_ligne(line, freq, common_words)
                logT.append(math.log(token, 10))
                logM.append(math.log(len(freq), 10))

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(logT[len(logT)//2:], logM[len(logM)//2:])

    b = slope
    k = 10**intercept
    print("Il y a {} tokens dans la collection.".format(token))
    print("Il y a {} mots dans le vocabulaire (taille du vocabulaire).".format(len(freq)))
    print("Paramètres de la loi de Heap: b={}, k={}, log(k)={}".format(slope,10**intercept,intercept))
    print("Pour 1 000 000 de tokens, il y aurait {} mots de vocabulaire.".format(int(k*10e6**b)))
    plt.plot(logT, logM)
    plt.savefig("logT_vs_logM_CS276.png")

    freqList = list(freq.values())
    freqList.sort(reverse=True)
    #print(rang)

    rangList = [k+1 for k in range(len(freqList))]

    plt.plot(rangList,freqList)
    plt.savefig("freq_vs_rg_CS276.png")
    #plt.show()

    logRang=[math.log10(k) for k in rangList]
    logFreq=[math.log10(f) for f in freqList]

    plt.plot(logRang, logFreq)
    plt.savefig("logFreq_vs_logRg_CS276.png")
    #plt.show()

print("*"*12)

# --------------------------------------
# -- Création des index
# --------------------------------------
from input import index_ligne

def save_index(index, name):
    with open('indexes/' + name + '.index', 'wb+') as f:
        pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)

doIndex = 0
try:
    doIndex = int(input("Do you want to build the index ?[0/1]\n"))
except ValueError:
    pass
if doIndex == 1:
    from input import vbe_index_ligne

    time_it = 0
    try:
        time_it = int(input("Do you want to time it ?[0/1]\n"))
    except ValueError:
        pass

    for folder in range(10):
        print("Création de l'index sur la collection CS276/{}.".format(folder))
        timeBeginningIndexCreation = time.time()
        index = dict()
        wordDic = dict()
        common_words = set()
        wordID = 0
        for docID, filename in enumerate(tqdm(os.listdir('data/CS276/'+str(folder)),desc="Index {}".format(folder))):
            with open('data/CS276/'+str(folder)+'/'+filename, "r") as file:
                line = file.readline()
                wordID = index_ligne(docID, line, index, wordDic, wordID, common_words)

        # Nombre de documents dans la collection
        collection_doc_nb = docID+1
        # On obtient un index de la forme {mot: [(docId1, frequency1), (docId2, frequency2), ...]}
        # Cela répond à la question 2.2 pour CS276
        for w_ID, docSet in index.items():
            index[w_ID] = [(docID, freq) for docID,freq in docSet.items()]
            index[w_ID].sort(key=lambda x : x[1], reverse=True)


        timeEndIndexCreation = time.time()

        if time_it == 1:
            print("Il a fallu {:.4f}s pour créer l'index {}.".format(timeEndIndexCreation - timeBeginningIndexCreation, folder))
        print("Enregistrement de l'index {0} dans 'indexes/CS276_{0}.index'".format(folder))
        save_index(index, "CS276_{}".format(folder))
        print("-"*12)

# --------------------------------------
# -- Création de l'index compressé
# --------------------------------------
doIndexCompression = 0
try:
    doIndexCompression = int(input("Do you want to build the index with Variable Byte Encoding compression ?[0/1]\n"))
except ValueError:
    pass
if doIndexCompression == 1:
    from input import vbe_index_ligne
    from output import save_index_vbe

    time_it = 0
    try:
        time_it = int(input("Do you want to time it ?[0/1]\n"))
    except ValueError:
        pass
    for folder in range(10):
        print("Création de l'index compressé sur la collection CS276/{}.".format(folder))
        timeBeginningIndexCreation = time.time()
        index = dict()
        wordDic = dict()
        wordID = 0
        for docID, filename in enumerate(tqdm(os.listdir('data/CS276/'+str(folder)),desc="Index {}".format(folder))):
            with open('data/CS276/'+str(folder)+'/'+filename, "r") as file:
                line = file.readline()
                wordID = vbe_index_ligne(docID, line, index, wordDic, wordID)

        # Nombre de documents dans la collection
        collection_doc_nb = docID+1
        for w_ID, docSet in index.items():
            index[w_ID] = sorted(docSet)
            for k in range(len(index[w_ID])-1, 0, -1):
                index[w_ID][k] = index[w_ID][k] - index[w_ID][k-1]

        timeEndIndexCreation = time.time()

        if time_it == 1:
            print("Il a fallu {:.4f}s pour créer l'index {}.".format(timeEndIndexCreation - timeBeginningIndexCreation, folder))
        print("Enregistrement de l'index {0} dans 'indexes/CS276_VBE_{0}.index'".format(folder))
        save_index_vbe("CS276_VBE_{}".format(folder), index, wordDic)
        print("Enregistrement de l'index {0} dans 'indexes/CS276_VBE_Ser_{0}.index'".format(folder))
        save_index(index, "CS276_VBE_Ser_{}".format(folder))

        """
        from output import encode
        for w_ID in index:
            for k in range(len(index[w_ID])):
                index[w_ID][k] = encode(index[w_ID][k])
        print("Enregistrement de l'index {0} dans 'indexes/CS276_VBE_Test_{0}.index'".format(folder))
        save_index(index, "CS276_VBE_Test_{}".format(folder))
        
        Le résultat obtenu dans cette configuration est plus volumineux encore que CS276_VBE_[folder]
        """

        print("-"*12)