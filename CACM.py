import sys
import re
import math
from matplotlib import pyplot as plt
import scipy.stats
import time
from tqdm import tqdm

# --------------------------------------
# -- Creation de Common Words
# --------------------------------------
common_words = set()

with open("data/CACM/common_words", "r") as common_words_list:
    for word in common_words_list:
        common_words.add(word[:-1])

# --------------------------------------
# -- Traitement linguistique
# --------------------------------------
doLanguageProcessing = 0
try:
    doLanguageProcessing = int(input("Do you want to do language processing ?[0/1]\n"))
except ValueError:
    pass
if doLanguageProcessing == 1:
    from input import linguistique_ligne, linguistique_author

    freq = dict()
    token = 0
    logT = []
    logM = []
    reading = False
    reading_authors = False

    with open("data/CACM/cacm.all", "r") as cacm:
        while True:
            line = cacm.readline()[:-1]
            if not line:
                break
            if line[0:2] == ".I":
                docID = int(line.split(' ')[1])
            if line[0:2] in [".T", ".W", ".K"]:
                reading = True
                reading_authors = False
            elif line[0:2] == ".A":
                reading = False
                reading_authors = True
            elif line[0] == ".":
                reading = False
                reading_authors = False
            elif reading:
                token += linguistique_ligne(line, freq, common_words)
                logT.append(math.log(token, 10))
                logM.append(math.log(len(freq), 10))
            elif reading_authors:
                token += linguistique_author()
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
    plt.savefig("results/logT_vs_logM_CACM.png")
    plt.show()

    freqList = list(freq.values())
    freqList.sort(reverse=True)
    #print(rang)

    rangList = [k+1 for k in range(len(freqList))]

    plt.plot(rangList,freqList)
    plt.savefig("results/freq_vs_rg_CACM.png")
    plt.show()

    logRang=[math.log10(k) for k in rangList]
    logFreq=[math.log10(f) for f in freqList]

    plt.plot(logRang, logFreq)
    plt.savefig("results/logFreq_vs_logRg_CACM.png")
    plt.show()

print("*"*12)

# --------------------------------------
# -- Création de l'index
# --------------------------------------
print("Index creation --")
from input import index_ligne, index_author

timeBeginningIndexCreation = time.time()
reading = False
reading_authors = False
index = dict()
wordDic = dict()
wordID = 0

with open("data/CACM/cacm.all", "r") as cacm:
    while True:
        line = cacm.readline()[:-1]
        if not line:
            break
        if line[0:2] == ".I":
            docID = int(line.split(' ')[1])
        if line[0:2] in [".T", ".W", ".K"]:
            reading = True
            reading_authors = False
        elif line[0:2] == ".A":
            reading = False
            reading_authors = True
        elif line[0] == ".":
            reading = False
            reading_authors = False
        elif reading:
            wordID = index_ligne(docID, line, index, wordDic, wordID, common_words)
        elif reading_authors:
            wordID = index_author(docID, line, index, wordDic, wordID, common_words)

# Nombre de documents dans la collection
collection_doc_nb = docID+1

# On obtient un index de la forme {motID: {(docID1, freqDoc1), (docID3, freqDoc3), (docID2, freqDoc2) ...}}
# Cela répond à la question 2.2 pour cacm
for w_ID, docSet in index.items():
    index[w_ID] = [(docID, freq) for docID,freq in docSet.items()]
    index[w_ID].sort(key=lambda x : x[1], reverse=True)
timeEndIndexCreation = time.time()
indexCreationTime = timeEndIndexCreation - timeBeginningIndexCreation
print("Il a fallu {:.4f}s pour créer l'index.".format(indexCreationTime))
print("il y a {} documents dans la collection".format(collection_doc_nb))

# --------------------------------------
# -- Sauvegarde de l'index
# --------------------------------------
doIndexSaving = 0
try:
    doIndexSaving = int(input("Do you want to save the index ?[0/1]\n"))
except ValueError:
    print("Not saved")
    pass
if doIndexSaving == 1:
    from output import index_saving
    index_saving('results/CACM.txt', "CACM", index, wordDic, indexCreationTime, withWordDic=True)

# --------------------------------------
# -- Requetes
# --------------------------------------

import boolean_search
doBooleanRequest = 1
while(doBooleanRequest):
    try:
        doBooleanRequest = int(input("Do you want to do a boolean request ?[0/1]\n"))
    except ValueError:
        print("No request")
        break
    if doBooleanRequest == 1:
        try:
            time_it = int(input("Do you want to time it ?[0/1]\n"))
        except ValueError:
            break       
        query = input("Please enter your request using infix form.\n")
        if time_it:
            res, qtime = boolean_search.boolean_search(query, collection_doc_nb, index, wordDic, True)
            print("Cela correspond aux documents :",res)
            print("Requete exécutée en {:.4f}s.".format(qtime))
        else:
            res =  boolean_search.boolean_search(query, collection_doc_nb, index, wordDic, False)
            print("Cela correspond aux documents :",res)
        
import vectorial_search
doVectorialRequest = 1
while(doVectorialRequest):
    try:
        doVectorialRequest = int(input("Do you want to do a vectorial request ?[0/1]\n"))
    except ValueError:
        print("No request")
        break
    if doVectorialRequest == 1:
        try:
            time_it = int(input("Do you want to time it ?[0/1]\n"))
        except ValueError:
            break   
        query = input("Please enter your request as the words to search.\n")
        if time_it:
            res, qtime = vectorial_search.vectorial_search(query, collection_doc_nb, index, wordDic, True)
            print("Cela correspond aux documents :",res)
            print("Requete exécutée en {:.4f}s.".format(qtime))
        else:
            res =  vectorial_search.vectorial_search(query, collection_doc_nb, index, wordDic, False)
            print("Cela correspond aux documents :",res)

import os
from input import parse_queries, parse_qrel
doEvaluation = 0
try:
    doEvaluation = int(input("Do you want to output evaluation parameters ?[0/1]\n"))
except ValueError:
    pass
if doEvaluation:
    with open('results/CACM_evaluation.txt', 'w+') as f:
        f.write("Evaluation de la collection CACM\n")
        f.write("\n# --------------------------------------\n# -- Performance\n# --------------------------------------\n")
        f.write("Index created in {:.4f}s.\n".format(indexCreationTime))
        try:
            size = os.stat("results/CACM.txt").st_size/1000
            f.write("Index size on disk {:.1f} kB.\n".format(size))
        except:
            f.write("Can not recover index size")
        b_query1 = "AND construction development"
        b_query2 = "AND medical OR information communication"
        b_query3 = "OR AND surface reconstruction AND logic language"
        b_query4 = "OR paper OR issue implementation"
        b_query5 = "AND paper AND issue implementation"
        f.write("\n")
        f.write("# Boolean Search\n")
        f.write("Query 1 ({}) answered in {:.6f}s.\n".format(b_query1,boolean_search.boolean_search(b_query1, collection_doc_nb, index, wordDic, True)[1]))
        f.write("Query 2 ({}) answered in {:.6f}s.\n".format(b_query2,boolean_search.boolean_search(b_query2, collection_doc_nb, index, wordDic, True)[1]))
        f.write("Query 3 ({}) answered in {:.6f}s.\n".format(b_query3,boolean_search.boolean_search(b_query3, collection_doc_nb, index, wordDic, True)[1]))
        f.write("Query 4 ({}) answered in {:.6f}s.\n".format(b_query4,boolean_search.boolean_search(b_query4, collection_doc_nb, index, wordDic, True)[1]))
        f.write("Query 5 ({}) answered in {:.6f}s.\n".format(b_query5,boolean_search.boolean_search(b_query5, collection_doc_nb, index, wordDic, True)[1]))
        f.write("\n")
        v_query1 = "construction development"
        v_query2 = "medical information communication"
        v_query3 = "surface reconstruction logic language"
        v_query4 = "paper issue implementation"
        f.write("# Vectorial Search\n")

        # query 1
        t_q1_tf_idf = vectorial_search.vectorial_search(v_query1, collection_doc_nb, index, wordDic, time_it=True, mode='tf-idf')[1]
        t_q1_tf_idf_norm = vectorial_search.vectorial_search(v_query1, collection_doc_nb, index, wordDic, time_it=True, mode='tf-idf-norm')[1]
        t_q1_freq_norm = vectorial_search.vectorial_search(v_query1, collection_doc_nb, index, wordDic, time_it=True, mode='freq-norm')[1]
        f.write("Query 1 ({}) answered in:\n\t{:.4f}s for tf_idf,\n\t{:.4f}s for normalized tf-idf,\n\t{:.4f}s in normalized freqency.\n".format(v_query1,t_q1_tf_idf,t_q1_tf_idf_norm,t_q1_freq_norm))

        # query 2
        t_q2_tf_idf = vectorial_search.vectorial_search(v_query2, collection_doc_nb, index, wordDic, time_it=True, mode='tf-idf')[1]
        t_q2_tf_idf_norm = vectorial_search.vectorial_search(v_query2, collection_doc_nb, index, wordDic, time_it=True, mode='tf-idf-norm')[1]
        t_q2_freq_norm = vectorial_search.vectorial_search(v_query2, collection_doc_nb, index, wordDic, time_it=True, mode='freq-norm')[1]
        f.write("Query 1 ({}) answered in:\n\t{:.4f}s for tf_idf,\n\t{:.4f}s for normalized tf-idf,\n\t{:.4f}s in normalized freqency.\n".format(v_query2,t_q2_tf_idf,t_q2_tf_idf_norm,t_q2_freq_norm))

        # query 3
        t_q3_tf_idf = vectorial_search.vectorial_search(v_query3, collection_doc_nb, index, wordDic, time_it=True, mode='tf-idf')[1]
        t_q3_tf_idf_norm = vectorial_search.vectorial_search(v_query3, collection_doc_nb, index, wordDic, time_it=True, mode='tf-idf-norm')[1]
        t_q3_freq_norm = vectorial_search.vectorial_search(v_query3, collection_doc_nb, index, wordDic, time_it=True, mode='freq-norm')[1]
        f.write("Query 1 ({}) answered in:\n\t{:.4f}s for tf_idf,\n\t{:.4f}s for normalized tf-idf,\n\t{:.4f}s in normalized freqency.\n".format(v_query3,t_q3_tf_idf,t_q3_tf_idf_norm,t_q3_freq_norm))

        # query 4
        t_q4_tf_idf = vectorial_search.vectorial_search(v_query4, collection_doc_nb, index, wordDic, time_it=True, mode='tf-idf')[1]
        t_q4_tf_idf_norm = vectorial_search.vectorial_search(v_query4, collection_doc_nb, index, wordDic, time_it=True, mode='tf-idf-norm')[1]
        t_q4_freq_norm = vectorial_search.vectorial_search(v_query4, collection_doc_nb, index, wordDic, time_it=True, mode='freq-norm')[1]
        f.write("Query 1 ({}) answered in:\n\t{:.4f}s for tf_idf,\n\t{:.4f}s for normalized tf-idf,\n\t{:.4f}s in normalized freqency.\n".format(v_query4,t_q4_tf_idf,t_q4_tf_idf_norm,t_q4_freq_norm))


        f.write("\n# --------------------------------------\n# -- Pertinence\n# --------------------------------------\n")

    queries = parse_queries('data/CACM/query.text', common_words)
    qrel_exp1 = dict()
    qrel_exp3 = dict()
    qrel_exp2 = dict()
    for queryID, query in tqdm(queries.items()):
        qrel_exp1[queryID] = vectorial_search.vectorial_search(query,
                                                              collection_doc_nb,
                                                              index, wordDic,
                                                              time_it=False,
                                                              mode='tf-idf')
        qrel_exp2[queryID] = vectorial_search.vectorial_search(query,
                                                              collection_doc_nb,
                                                              index, wordDic,
                                                              time_it=False,
                                                              mode='tf-idf-norm')
        qrel_exp3[queryID] = vectorial_search.vectorial_search(query,
                                                              collection_doc_nb,
                                                              index, wordDic,
                                                              time_it=False,
                                                              mode='freq-norm')

    qrel_real = parse_qrel('data/CACM/qrels.text')
    """
    print('QREL EXP\n', qrel_exp1)
    print('QREL EXP\n', qrel_exp2)
    print('QREL EXP\n', qrel_exp3)
    print('QREL REAL\n', qrel_real)
    """
    import evaluation_vect
    for query, answer in qrel_exp1.items():
        if len(answer) > 0:
            evaluation_vect.plot_precision_recall(answer, qrel_real[query])
