import pandas as pd
from operator import index, itemgetter 
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
    elif(column == "10"):
        df[column] = "*"
    else:
        max_gen = 1
    return df,max_gen

def fly(df,qid,w_qid,k):
    index_max = 1
    while(check_ano(df,qid) < k):
        compute_occu = order_occu(df,qid)
        val = compute_occu[0]
        total = compute_occu[1]
        tab_distinct = []
        for q in range(0,len(qid)):
            if total[q][0] >= k:
                tab_distinct.append(0)
            else:
                tab_distinct.append(len(total[q]))
        print(check_ano(df,qid))
        #WEIGHTS
        for w in range(5,0,-1):
            indices = [i for i, x in enumerate(w_qid) if x == w]
            if(len(indices) > 0):
                index_max_local = max(range(len(indices)), key=[tab_distinct[i] for i in indices].__getitem__)
                if([tab_distinct[i] for i in indices][index_max_local] > 0):
                    index_max = tab_distinct.index([tab_distinct[i] for i in indices][index_max_local])
                    break
        gen = generalize(df,qid[index_max])
        if(gen[1] > 0):
            #delete all seq which occu < k
            for q in range(0,len(qid)):
                for i in range(0,len(total[q])):
                    if(total[q][i] < k):
                        df = df[getattr(df,qid[q]) != val[q][i]]
                    else:
                        break
                break
        else:
            df = gen[0]
    return df

#Run
def run(df,k,qid,w_qid):
    df_final = fly(df,qid,w_qid,k)
    print(df_final)
    return check_ano(df_final,qid)

df = read_file('test_algo/data/adult.csv', ';')
k = 16193
qid = ["10","13"]
w_qid = [4,2]
print(run(df,k,qid,w_qid))