from cmath import nan
from numpy import NaN
import pandas as pd
import itertools

def read_file(path, delim):
    csv = pd.read_csv(path, sep=delim)
    return csv

def check_ano(df,qid):
    res = get_class(df,qid)
    return min(res)

def get_class(df,qid):
    datas_qid = df[qid]
    dups_shape = datas_qid.pivot_table(columns=qid, aggfunc='size')
    return dups_shape

def generalize(df,qid,lvl):
    if qid == "zip":
        if lvl == 1:
            df["zip"] = df["canton"]
        elif lvl == 2:
            df["zip"] = df["pays"]
    elif qid == "age":
        if lvl == 1:
            df["age"] = df["age_dizaine"]
        elif lvl == 2:
            df["age"] = df["age_split"]
    elif qid == "illness":
        if lvl == 1:
            df["illness"] = df["general_illness"]
    return df

def occu(df,qid):
    tab_dict = []
    for q in qid:
        index_tab = df[q].value_counts(ascending = True).index.tolist()
        occu_tab = df[q].value_counts(ascending = True).tolist()
        tab_dict.append(dict(zip(index_tab,occu_tab)))
    return tab_dict

def algo(df_init,qid,max_gen,weigths,k):
    list_comb = []
    for g in max_gen:
        list_comb.append(list(range(0,g+1)))
    list_comb = list(itertools.product(*list_comb))
    print("Start")
    cost = []
    ok = NaN
    for c in list_comb:
        if(ok is not NaN):
            if(len([item1 for item1, item2 in zip(c, ok) if item1 >= item2]) == len(qid)):
                continue
        df = df_init.copy()
        for q in range(0,len(qid)):
            df = generalize(df,qid[q],c[q])
        count_supp = 0
        if(check_ano(df,qid) < k):
            size_class = get_class(df,qid)
            for s in size_class:
                if(s < k):
                    count_supp += s
        sum_w = 0
        for q2 in range(0,len(qid)):
            sum_w += sum(weigths[q2][0:c[q2]])
        print(f"\nQID : {qid}, lvl of generalization : {c}, number of suppression : {count_supp}, total cost : {count_supp * sum(sum(weigths,[])) + (len(df)-count_supp) * sum_w}, k before suppression = {check_ano(df,qid)}")
        cost.append(count_supp * sum(sum(weigths,[])) + (len(df)-count_supp) * sum_w)
        if(count_supp == 0):
            ok = c
        else:
            ok = NaN
            #break
    return cost


df = read_file("test_algo/data/complete_data_test.csv",",")
qid = ["age","illness"]
max_gen = [2,1]
weigths = [[3,4],[6]]
k = 7
algo(df,qid,max_gen,weigths,k)