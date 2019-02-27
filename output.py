"""
Output functions
"""

def save_index(filename, name, index, wordDic, time, withWordDic=True):
    with open(filename, 'w+') as f:
        f.write("Index {} created in {:.4f}s.\n\n".format(name,time))
        if withWordDic:
            f.write("Word to WordID - on {} words\n".format(len(wordDic)))
            for k,v in wordDic.items():
                f.write(k + " " + str(v)+ "\n")
            f.write("# END Word to WordID\n\n")
        f.write("Index - on {} words\n".format(len(wordDic)))
        for k,v in index.items():
            f.write(str(k) + " : " + doubletList2string(v)+ "\n")
        f.write("# END Index\n")

def doubletList2string(l):
    s = ""
    for k in l[:-1]:
        s += "({}, {}) ".format(k[0], k[1])
    s += "({}, {})".format(l[-1][0], l[-1][1])
    return s

def save_index_vbe(filename, index, wordDic, withWordDic=False):
    with open('indexes/' + filename + '.index', 'wb+') as f:
        if withWordDic:
            f.write(encode(len(wordDic)))
            for k,v in wordDic.items():
                encoded = k.encode('utf8')
                f.write(encode(len(encoded)))
                f.write(encoded)
                f.write(encode(v))
        f.write(encode(len(wordDic)))
        for k,v in index.items():
            f.write(encode(k))
            f.write(encode(len(v)))
            for d in v:
                f.write(encode(d))

def dec2bin(d,nb=7):
    """
    dec2bin(d,nb=0): conversion nombre entier positif ou nul -> chaîne binaire (si nb>0, complète à gauche par des zéros)
    """
    if d==0:
        b=b"0"
    else:
        b=b""
        while d!=0:
            if d % 2 == 0:
                b=b'0'+b
            else:
                b=b'1'+b
            d=d>>1
    return b.zfill(nb)

def encode(d,nb=7,two2nb=128):
    """
    Variable byte encoding
    """
    if d < two2nb:
        return b'1'+dec2bin(d,nb)
    else:
        res = b'1'+dec2bin(d%two2nb,nb)
        d //= two2nb
        while d != 0:
            res = b'0'+dec2bin(d%two2nb,nb) + res
            d //= two2nb
    return res