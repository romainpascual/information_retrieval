"""
Aux functions
"""

def merge_list_index(index_list, l):
    i, j , n, m = 0, 0, len(index_list), len(l)
    while i < n and j < m:
        if index_list[i][0] == l[j][0]:
            index_list[i] = (index_list[i][0], l[j][1]+index_list[i][1])
            i += 1
            j += 1
        elif index_list[i][0] < l[j][0]:
            i += 1
        else: # index_list[i][0] > l[j][0]:
            index_list.insert(i,l[j])
            j += 1
    if j < m:
        index_list.extend(l[j:])