"""
Output functions
"""

def index_saving(filename, name, index, wordDic, time=0, withWordDic=True):
    with open(filename, 'w+') as f:
        if time > 0:
            f.write("Index {} created in {:.4f}s.\n\n".format(name,time))
        else:
            f.write("Index {}.\n\n".format(name))
        if withWordDic:
            f.write("Word to WordID - on {} words\n".format(len(wordDic)))
            for k,v in wordDic.items():
                f.write(k + " " + str(v)+ "\n")
            f.write("# END Word to WordID\n\n")
            f.write("Index - on {} words\n".format(len(wordDic)))
        for k,v in index.items():
            f.write(str(k) + " : " + Item2string(v)+ "\n")
        f.write("# END Index\n")

def Item2string(l):
    s = ""
    if type(l[0]) == int:
        for k in l[:-1]:
            s += "{} ".format(k)
        s += str(l[-1])
    elif len(l[0])==2:
        for k in l[:-1]:
            s += "({}, {}) ".format(k[0], k[1])
        s += "({}, {})".format(l[-1][0], l[-1][1])
    return s

def index_saving_vbe(filename, index, wordDic, withWordDic=False):
    with open(filename, 'wb+') as f:
        if withWordDic:
            f.write(encode(1))
            f.write(encode(len(wordDic)))
            for k,v in wordDic.items():
                encoded = k.encode('utf8')
                f.write(encode(len(encoded)))
                f.write(encoded)
                f.write(encode(v))
            f.write(encode(len(wordDic)))
        else:
            f.write(encode(0))
        for k,v in index.items():
            f.write(encode(k))
            f.write(encode(len(v)))
            for d in v:
                f.write(encode(d))

code = dict()

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
    if d not in code:
        if d < two2nb:
            res = b'1'+dec2bin(d,nb)
        else:
            copy = d
            res = b'1'+dec2bin(copy%two2nb,nb)
            copy //= two2nb
            while copy != 0:
                res = b'0'+dec2bin(copy%two2nb,nb) + res
                copy //= two2nb
        code[d] = res
    return code[d]