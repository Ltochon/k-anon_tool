from typing import final
from numpy import array
import numpy as np
import pandas as pd
from operator import itemgetter
import operator 

def generalize(level, data, qid2):
    if(level != 0):
        if(qid2 != 'sex'):
            if(qid2 != 'zipcode'):
                tab = []
                for x in range(len(data)):
                    tab.append(str(data[qid2][x])[:-1])
                data[qid2] = tab
            else:
                if(level == 1):
                    data[qid2] = data['region']
                else:
                    data[qid2] = data['canton']
        else:
            data[qid2] = ['X'] * len(data)
    return data   

def order_solutions(tab,priority,max_level):
    return_tab = []
    for sol in tab:
        total_cost = 0
        for index in range(len(sol)):
            total_cost = total_cost + (sol[index]/max_level[index])**priority[index]
        total_cost = 1/len(max_level) * total_cost
        return_tab.append(total_cost)
    index_order = list(np.argsort(return_tab))
    return_tab_ordered = [tab[i] for i in index_order]
    return return_tab_ordered  


cmpt_qid = 0
deg_gen = [1,1,2]
priority_deg = [3,1,1] ##Higher is the level, less must be the change
qid = ["birth_year","sex","zipcode"]
tab_res = []
k = 5
##STEP1
print("\nSTEP 1\n")
while cmpt_qid < len(qid):
    cmpt_prof = 0
    while(cmpt_prof <= deg_gen[cmpt_qid]):
        datas = pd.read_csv('test_algo/data/records.csv')
        generalize(cmpt_prof,datas,qid[cmpt_qid])
        datas_qid = datas[qid[cmpt_qid]].to_frame()
        dups_shape = datas_qid.pivot_table(columns=qid[cmpt_qid], aggfunc='size')
        print(qid[cmpt_qid], cmpt_prof, " : Smallest class size : ",min(dups_shape))
        if(min(dups_shape) >= k):
            tab_res.append(cmpt_prof)
            cmpt_prof = deg_gen[cmpt_qid] + 1
        else:
            cmpt_prof = cmpt_prof + 1
    cmpt_qid = cmpt_qid + 1

tab_res_save = tab_res
tab_res = []
cmpt = 0
print("\nSTEP 2\n")

##STEP2
i = 0 #to change
while(i < 2):
    j = i + 1
    while(j < len(qid)):
        start_prof = [0,0,0]
        tab_res.append([])
        ok = False
        while(all(i >= 0 for i in list(map(list(map(operator.sub, deg_gen, start_prof)).__getitem__,[i,j])))):
            datas = pd.read_csv('test_algo/data/records.csv')
            data = generalize(start_prof[i],datas,qid[i])
            data = generalize(start_prof[j],data,qid[j])
            datas_qid = datas[list(map(qid.__getitem__, [i,j]))]
            dups_shape = datas_qid.pivot_table(columns=list(map(qid.__getitem__, [i,j])), aggfunc='size')
            print(list(map(qid.__getitem__, [i,j])), list(map(start_prof.__getitem__,[i,j])), " : Smallest class size : ",min(dups_shape))
            if(min(dups_shape) >= k):
                tab_res[cmpt].append([start_prof[i],start_prof[j]])
                ok = True
                start_prof[i] = deg_gen[i] + 1
            else:
                tab = list(map(list(map(operator.sub, deg_gen, start_prof)).__getitem__,[i,j]))
                index = [idx for idx in range(len(tab)) if tab[idx] > 0]
                if(index[0] == 0):
                    start_prof[i] = start_prof[i] + 1
                else:
                    start_prof[j] = start_prof[j] + 1
        if(not ok):
            tab_res[cmpt].append([])
        j = j + 1
        cmpt = cmpt + 1
    i = i + 1
print(tab_res)

final_tab = [0]*len(qid)
a = 0
cmpt_pair_a = 0
cmpt_pair_b = 1
max = len(qid)-1
max_a = len(qid)-1
for comp in range(len(qid)):
    
    for case in tab_res[comp]:
        if(final_tab[a] < case[0]):
            final_tab[a] = case[0]
        if(final_tab[cmpt_pair_b] < case[1]):
            final_tab[cmpt_pair_b] = case[1]
    if(cmpt_pair_a == max_a):
        a = a + 1
        cmpt_pair_a  = 0
        max_a = max_a - 1
    if(cmpt_pair_b == max):
        cmpt_pair_b = a + 1
    cmpt_pair_b = cmpt_pair_b + 1
    cmpt_pair_a = cmpt_pair_a + 1
print(final_tab)

##to do
solutions = []
print("\nSTEP 3\n")
for i in range(deg_gen[0] - final_tab[0] + 1):
    for j in range(deg_gen[1] - final_tab[1]+ 1):
        for l in range(deg_gen[2] - final_tab[2]+ 1):
            datas = pd.read_csv('test_algo/data/records.csv')
            datas = generalize(final_tab[2] + l,datas,qid[2])
            datas = generalize(final_tab[0] + i,datas,qid[0])
            datas = generalize(final_tab[1] + j,datas,qid[1])
            
            datas_qid = datas[qid]
            dups_shape = datas_qid.pivot_table(columns=qid, aggfunc='size')
            print(qid, final_tab[0] + i,final_tab[1] + j, final_tab[2] + l, " : Smallest class size : ",min(dups_shape))
            if(min(dups_shape) >= k):
                solutions.append([final_tab[0] + i,final_tab[1] + j, final_tab[2] + l])


print(order_solutions(solutions, priority_deg, deg_gen))
