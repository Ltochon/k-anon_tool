import json
from typing import Type
from numpy import NaN
import pandas as pd

def create_lattice(max_gen): #creation of the complete lattice
    current = [tuple(len(max_gen)*[0])] #init first node
    tree = [] #init complete tree
    while current != []:
        tree.append(current) 
        copy = current 
        next_lvl = []
        for elem in range(len(copy)): #for each element of the current depth level
            l = list(copy[elem]) #get all value inside a node
            for i in range(len(l)):
                new_l = l.copy()
                new_l[i] += 1 #try to add 1 to each node's values
                if(new_l[i] <= max_gen[i]): #if +1 respects the max generalization level
                    if(tuple(new_l) not in next_lvl): #if the new node doesn't exist
                        next_lvl.append(tuple(new_l))  
        current = next_lvl #current become the next depth level
    return tree

def read_file(path, delim):
    csv = pd.read_csv(path, sep=delim)
    return csv

def check_ano(df,qid):
    res = get_class(df,qid)
    return min(res)

def get_class(df,qid): #create equivalence classes
    datas_qid = df[qid]
    dups_shape = datas_qid.pivot_table(columns=qid, aggfunc='size') #create classes
    return dups_shape

def generalize(df,qid,lvl,type_inp,lattice,max_gen):
    scaled = max_gen - lvl #to change !
    if(scaled < max_gen): #if a generalization is necessary
        if type_inp == 'int': 
            if(scaled != 0): #not max generalization
                i = 0
                rule = json.loads(lattice)[str(scaled)] #load the 2D array of integer generalization law
                tab_rule = []
                for r in rule: #split string into ranges
                    temp_s = r.split(" ")
                    tab_rule.append([temp_s[1],temp_s[3]]) #append lower and upper limit
                while(i < len(df)): #foreach value
                    for r2 in tab_rule: #test each rule
                        if(int(df.at[i,qid]) >= int(r2[0]) and int(df.at[i,qid]) <= int(r2[1])):
                            df.at[i,qid] = "[ " +  r2[0] + " ; " + r2[1] + " ]"
                            break
                    i = i + 1
            else: #max generalization (= '*')
                i = 0
                while(i < len(df)): #foreach value
                    df.at[i,qid] = '*'
                    i += 1
    return df

def occu(df,qid):
    tab_dict = []
    for q in qid:
        index_tab = df[q].value_counts(ascending = True).index.tolist() #get array of index
        occu_tab = df[q].value_counts(ascending = True).tolist() #get array of value in the same order than index
        tab_dict.append(dict(zip(index_tab,occu_tab))) #create dictionnary
    return tab_dict

def algo_web(df_init,qid,max_gen,weigths,k,max_supp,types,lattice):
    list_comb = create_lattice(max_gen)
    list_cost = []
    current_level = [round(len(list_comb)/2)-1] #start of binary search
    stop = False
    while not stop:
        found_no_supp = False
        cost = []
        for c in list_comb[current_level[len(current_level)-1]]: #for all node in lattice's current level
            df = df_init.copy() #create copy to work with it
            for q in range(0,len(qid)): #foreach qid
                df = generalize(df,qid[q],c[q],types[q],lattice[q],max_gen[q]) #apply generalization level
            count_supp = 0
            ano = check_ano(df,qid) #get global k-anonymity
            if(ano < k): 
                size_class = get_class(df,qid)
                for s in size_class: #for all equivalence classes
                    if(s < k): #if class size is less than k
                        count_supp += s #add class size to total suppression count
                ano = k
            if(count_supp/len(df)*100 <= max_supp): #if suppression rate is OK
                found_no_supp = True #solution is OK
            sum_w = 0
            for q2 in range(0,len(qid)): #calculate total cost with custom weights
                sum_w += sum(weigths[q2][0:c[q2]])
            print(f"\nQID : {qid}, lattice : {current_level[len(current_level)-1]}, lvl of generalization : {c}, supp : {count_supp/len(df)*100}%, total cost : {count_supp * sum(sum(weigths,[])) + (len(df)-count_supp) * sum_w}, k before suppression = {check_ano(df,qid)}")
            cost.append([df,c,round(count_supp * sum(sum(weigths,[])) + (len(df)-count_supp) * sum_w,2),ano,round(count_supp/len(df)*100,2)]) #cost storage
        if(found_no_supp): #if solution is OK
            if(len(current_level) == 1):
                current_level.append(round(len(list_comb)/4)-1) #go to lower generalization level
            else:
                if((current_level[len(current_level)-1] + current_level[len(current_level)-1])/2 not in current_level): #go to lower generalization level
                    current_level.append((current_level[len(current_level)-1] + current_level[len(current_level)-1])/2)
                else: #test if no more new lattice level available
                    stop = True
        else: #solution is not OK
            if(len(current_level) == 1):
                current_level.append(3*round(len(list_comb)/4)-1)#go to greater generalization level
            else:
                if((current_level[len(current_level)-1] + current_level[len(current_level)-1])/2 not in current_level): #go to greater generalization level
                    current_level.append((current_level[len(current_level)-1] + current_level[len(current_level)-1])/2)
                else: #test if no more new lattice level available
                    stop = True
        list_cost.append(cost)
    return list_cost

###
#Example of run parameter
###

# df = read_file("test_algo/data/complete_data_test.csv",",")
# qid = ["age","zip"]
# max_gen = [2,2]
# weigths = [[3,4],[5,6]]
# k = 7
# max_supp = 0.1
# print(algo(df,qid,max_gen,weigths,k,max_supp))