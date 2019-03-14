"""
Evaluation for vectorial search
"""
from matplotlib import pyplot as plt

def precision_recall(found, pertinents):
    pertinent_found = 0
    precision_recall  = []
    for k in range(len(found)):
        f = found[k]
        if f in pertinents:
            pertinent_found += 1
        recall = pertinent_found // len(pertinents)
        precision = pertinent_found // (k+1)
        precision_recall.append([recall, precision])
    return precision_recall

def plot_precision_recall(found, pertinents):
    p_r = precision_recall(found, pertinents)
    p_r.sort(key=lambda x : x[0])

    x = []
    y = []

    for k in range(len(p_r)-1):
        to_keep = True
        for l in range(k,len(p_r)):
            if p_r[l][1] > p_r[k][1] :
                to_keep = False
                break
        if to_keep:
            x.append(p_r[k][0])
            y.append(p_r[k][1])

    plt.plot(x,y)
    plt.show()

def E_measure(precision, recall, alpha=-1):
    if alpha == -1:
        betha = precision/recall
        alpha = 1/(betha*betha+1)
    E = 1 - 1/( alpha/precision + (1-alpha)/recall)
    return E

def E_measure_mean(found, pertinents):
    p_r = precision_recall(found, pertinents)
    total_E = 0
    for [precision,recall] in p_r:
        total_E += E_measure(precision,recall)
    return total_E / len(p_r)

def F_measure(precision, recall, alpha=-1):
    return 1 - E_measure(precision, recall, alpha)

def F_measure_mean(found, pertinents):
    p_r = precision_recall(found, pertinents)
    total_F = 0
    for [precision,recall] in p_r:
        total_F += F_measure(precision,recall)
    return total_F / len(p_r)

def R_precision(x):
    """

    """