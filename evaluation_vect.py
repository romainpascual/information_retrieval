"""
Evaluation for vectorial search
"""

def E_measure(precision, rappel, alpha=-1):
    if alpha == -1:
        betha = precision/rappel
        alpha = 1/(betha*betha+1)
    E = 1 - 1/( alpha/precision + (1-alpha)/rappel)
    return E

def F_measure(precision, rappel, alpha=-1):
    return 1 - E_measure(precision, rappel, alpha)

def R_precision(x):
    """

    """