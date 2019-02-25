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
            f.write(str(k) + list2string(v)+ "\n")
        f.write("# END Word to WordID\n")

def list2string(l):
    s = ""
    for k in l[:-1]:
        s += str(k) + " "
    s += str(l[-1])
    return s