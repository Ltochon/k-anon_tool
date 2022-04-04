import pandas as pd
from operator import index, itemgetter 
def read_file(path, delim):
    csv = pd.read_csv(path, sep=delim)
    return csv

def check_ano(df,qid):
    datas_qid = df[qid]
    dups_shape = datas_qid.pivot_table(columns=qid, aggfunc='size')
    return min(dups_shape)

def generalize(df,qid,lvl):
    if qid == "zip":
        if lvl == 1:
            df["zip"] = df["canton"]
        elif lvl == 2:
            df["zip"] = df["pays"]
    return df

def occu(df,qid):
    for q in qid:
        index_tab = df[q].value_counts(ascending = True).index.tolist()
        occu_tab = df[q].value_counts(ascending = True).tolist()
    return dict(zip(index_tab,occu_tab))

def algo(df,qid,max_gen,weigths,k):
    print("Start")
    cost = []
    for q in range(0,len(qid)):
        for g in range(0,max_gen[q]+1):
            df = generalize(df,qid[q],g)
            count_supp = 0
            if(check_ano(df,qid) < k):
                dict_occu = occu(df,qid)
                for d in dict_occu:
                    if(dict_occu[d] < k):
                        count_supp += dict_occu[d]
            print(f"\nQID : {qid[q]}, lvl of generalization : {g}, number of suppression : {count_supp}, total cost : {count_supp * sum(weigths[q]) + len(df) * sum(weigths[q][0:g])}")
            cost.append(count_supp * sum(weigths[q]) + len(df) * sum(weigths[q][0:g])) 
    return cost


df = read_file("test_algo/data/complete_data_test.csv",",")
qid = ["zip"]
max_gen = [2]
weigths = [[2,3]]
k = 10
algo(df,qid,max_gen,weigths,k)