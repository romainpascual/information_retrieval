"""
Evaluation for vectorial search
"""
from matplotlib import pyplot as plt
from tqdm import tqdm
from input import parse_queries, parse_qrel
import vectorial_search

def precision_recall(found, pertinents):
    pertinent_found = 0
    precision_recall  = []
    for k in range(len(found)):
        f = found[k]
        if f in pertinents:
            pertinent_found += 1
        recall = pertinent_found / len(pertinents)
        precision = pertinent_found / (k+1)
        precision_recall.append([recall, precision])
    return precision_recall

def plot_precision_recall(p_r,filename):
    p_r.sort(key=lambda x : x[0])

    x = []
    y = []

    for k in range(len(p_r)-1):
        to_keep = True
        for l in range(k):
            if p_r[l][1] == p_r[k][1]:
                to_keep = False
                break
        for l in range(k,len(p_r)):
            if p_r[l][1] > p_r[k][1] :
                to_keep = False
                break
        if to_keep:
            x.append(p_r[k][0])
            y.append(p_r[k][1])
    plt.step(x,y)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.savefig('precision_recall/'+filename+'.png')
    plt.clf()

def E_measure(precision, recall, alpha=-1):
    if precision == 0 or recall == 0:
        return None
    if alpha == -1:
        betha = precision/recall
        alpha = 1/(betha*betha+1)
    E = 1 - 1/( alpha/precision + (1-alpha)/recall)
    return E

def E_measure_mean(p_r):
    total_E = 0
    non_none_values = 0
    for [precision,recall] in p_r:
        E = E_measure(precision,recall)
        if E is not None:
            total_E += E
            non_none_values += 1
    if non_none_values == 0:
        return 0
    return total_E / non_none_values

def F_measure(precision, recall, alpha=-1):
    if precision == 0 or recall == 0:
        return None
    return 1 - E_measure(precision, recall, alpha)

def F_measure_mean(p_r):
    total_F = 0
    non_none_values = 0
    for [precision,recall] in p_r:
        F = F_measure(precision,recall)
        if F is not None:
            total_F += F
            non_none_values += 1
    if non_none_values == 0:
        return 0
    return total_F / len(p_r)

def process_answer(found, pertinents, filename):
    p_r = precision_recall(found,pertinents)
    plot_precision_recall(p_r,filename)
    E = E_measure_mean(p_r)
    F = F_measure_mean(p_r)
    return E,F

def process_vect_eval(common_words, collection_doc_nb, index, wordDic, time_it=False):
    res = dict()
    queries = parse_queries('data/CACM/query.text', common_words)
    qrel_exp1 = dict()
    qrel_exp3 = dict()
    qrel_exp2 = dict()
    for queryID, query in tqdm(queries.items()):
        qrel_exp1[queryID] = vectorial_search.vectorial_search(query,
                                                              collection_doc_nb,
                                                              index, wordDic,
                                                              time_it,
                                                              mode='tf-idf')
        qrel_exp2[queryID] = vectorial_search.vectorial_search(query,
                                                              collection_doc_nb,
                                                              index, wordDic,
                                                              time_it,
                                                              mode='tf-idf-norm')
        qrel_exp3[queryID] = vectorial_search.vectorial_search(query,
                                                              collection_doc_nb,
                                                              index, wordDic,
                                                              time_it,
                                                              mode='freq-norm')

    qrel_real = parse_qrel('data/CACM/qrels.text')

    exp1 = 0
    E_tot1 = 0
    F_tot1 = 0
    for query, expected in qrel_real.items():
        answer = qrel_exp1[query]
        if len(answer) > 0:
            exp1 += 1
            E, F = process_answer(answer, expected, "{}_tf_ifd".format(query))
            E_tot1 += E
            F_tot1 += F
    res['Emoy tf-idf'] = E_tot1 / exp1
    res['Fmoy tf-idf'] = F_tot1 / exp1
    
    exp2 = 0
    E_tot2 = 0
    F_tot2 = 0
    for query, expected in qrel_real.items():
        answer = qrel_exp2[query]
        if len(answer) > 0:
            exp2 += 1
            E, F = process_answer(answer, expected, "{}_tf_ifd_norm".format(query))
            E_tot2 += E
            F_tot2 += F
    res['Emoy tf-idf-norm'] = E_tot2 / exp2
    res['Fmoy tf-idf-norm'] = F_tot2 / exp2

    exp3 = 0
    E_tot3 = 0
    F_tot3 = 0
    for query, expected in qrel_real.items():
        answer = qrel_exp3[query]
        if len(answer) > 0:
            exp3 += 1
            E, F = process_answer(answer, expected, "{}_freq_norm".format(query))
            E_tot3 += E
            F_tot3 += F
    res['Emoy freq-norm'] = E_tot3 / exp3
    res['Fmoy freq-norm'] = F_tot3 / exp3

    return res