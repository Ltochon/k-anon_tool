from numpy import NaN
import pandas as pd
import samarati_lattice
from samarati_lattice import create_lattice

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

def algo(df_init,qid,max_gen,weigths,k,max_supp):
    list_comb = create_lattice(max_gen)
    print(list_comb)
    print("Start")
    list_cost = []
    current_level = [round(len(list_comb)/2)-1]
    stop = False
    while not stop:
        found_no_supp = False
        cost = []
        for c in list_comb[current_level[len(current_level)-1]]:
            df = df_init.copy()
            for q in range(0,len(qid)):
                df = generalize(df,qid[q],c[q])
            count_supp = 0
            if(check_ano(df,qid) < k):
                size_class = get_class(df,qid)
                for s in size_class:
                    if(s < k):
                        count_supp += s
            if(count_supp/len(df) <= max_supp):
                found_no_supp = True
            sum_w = 0
            for q2 in range(0,len(qid)):
                sum_w += sum(weigths[q2][0:c[q2]])
            print(f"\nQID : {qid}, lattice : {current_level[len(current_level)-1]}, lvl of generalization : {c}, supp : {count_supp/len(df)*100}%, total cost : {count_supp * sum(sum(weigths,[])) + (len(df)-count_supp) * sum_w}, k before suppression = {check_ano(df,qid)}")
            cost.append([c,count_supp * sum(sum(weigths,[])) + (len(df)-count_supp) * sum_w])
        if(found_no_supp):
            if(len(current_level) == 1):
                current_level.append(round(len(list_comb)/4)-1)
            else:
                if((current_level[len(current_level)-1] + current_level[len(current_level)-1])/2 not in current_level):
                    current_level.append((current_level[len(current_level)-1] + current_level[len(current_level)-1])/2)
                else:
                    stop = True
        else:
            if(len(current_level) == 1):
                current_level.append(3*round(len(list_comb)/4)-1)
            else:
                if((current_level[len(current_level)-1] + current_level[len(current_level)-1])/2 not in current_level):
                    current_level.append((current_level[len(current_level)-1] + current_level[len(current_level)-1])/2)
                else:
                    stop = True
        list_cost.append(cost)
    return list_cost


df = read_file("test_algo/data/complete_data_test.csv",",")
qid = ["age","zip"]
max_gen = [2,2]
weigths = [[3,4],[5,6]]
k = 7
max_supp = 0.1
print(algo(df,qid,max_gen,weigths,k,max_supp))