import sys
import re

index = dict()
common_words = set()

token = 0

with open("data/CACM/common_words", "r") as common_words_list:
    for word in common_words_list:
        common_words.add(word[:-1])


def traiter_ligne(docID, line):
    words = re.split('[^a-z0-9]', line.lower())
    token = 0
    for word in words:
        token += 1
        if word not in common_words:
            try:
                index[word].add(docID)
            except KeyError:
                index[word] = {docID}
    return token

reading = False
while True:
    line = sys.stdin.readline()[:-1]
    if not line:
        break
    if line[0:2] == ".I":
        docID = int(line.split(' ')[1])
    if line[0:2] in [".T", ".W", ".K"]:
        reading = True
    elif line[0] == ".":
        reading = False
    elif reading:
        token += traiter_ligne(docID, line)

for word, value in index.items():
    index[word] = sorted(list(value))

print(index)

print("Il y a {} tokens dans la collection.".format(token))
print("Il y a {} mots dans le vocabulaire.".format(len(index)))
