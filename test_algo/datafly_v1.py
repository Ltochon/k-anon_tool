from os import sep
from turtle import pd


import pandas as pd
def read_file(path, delim):
    csv = pd.read_csv(path, sep=delim)
    return csv

def check_ano(df,qid):
    datas_qid = df[qid]
    dups_shape = datas_qid.pivot_table(columns=qid, aggfunc='size')
    return min(dups_shape)

def order_occu(df,qid):
    occu_tab = []
    index_tab = []
    for q in qid:
        index_tab.append(df[q].value_counts(ascending = True).index.tolist())
        occu_tab.append(df[q].value_counts(ascending = True).tolist())
    return index_tab,occu_tab

def generalize(df,column):
    #custom generalization to do
    max_gen = 0
    if(column == "13"):
        df[column] = df["15"]
    else:
        max_gen = 1
    return df,max_gen

def fly(df,qid,val,total,k):
    index_max = 1

    while(check_ano(df,qid) < k):
        tab_distinct = []
        for q in range(0,len(qid)):
            if total[q][0] >= k:
                tab_distinct.append(0)
            else:
                tab_distinct.append(len(total[q]))
        index_max = max(range(len(tab_distinct)), key=tab_distinct.__getitem__)
        gen = generalize(df,qid[index_max])
        if(gen[1] > 0):
            break
        else:
            df = gen[0]
    return df

#Run
df = read_file('test_algo/data/adult.csv', ';')
qid = ["10","13"]
k = 4
compute_occu = order_occu(df,qid)
val = compute_occu[0]
total = compute_occu[1]
df_final = fly(df,qid,val,total,k)
print(df_final)
