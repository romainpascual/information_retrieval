"""
Output functions
"""

def save_index(filename, name, index, wordDic, time, withWordDic=True):
    with open(filename, 'w+') as f:
        f.write("Index {} created in {:.4f}s.\n\n".format(name,time))
        if withWordDic:
            f.write("Word to WordID - on {} words\n".format(len(wordDic)))
            for k,v in wordDic.items():
                f.write(k + str(v)+ "\n")
            f.write("# END Word to WordID\n\n")
        f.write("Index - on {} words".format(len(wordDic)))
        for k,v in index.items():
            f.write(str(k) + doubletList2string(v)+ "\n")
        f.write("# END Word to WordID\n")

def doubletList2string(l):
    s = ""
    for k in l[:-1]:
        s += "({}, {}) ".format(k[0], k[1])
    s += "({}, {})".format(l[-1][0], l[-1][1])
    return s