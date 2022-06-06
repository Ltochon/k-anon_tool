import json
import math
import pandas as pd

class SSW:
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
        res = SSW.get_class(df,qid)
        return min(res)

    def get_class(df,qid): #create equivalence classes
        datas_qid = df[qid]
        dups_shape = datas_qid.pivot_table(columns=qid, aggfunc='size') #create classes
        return dups_shape

    def generalize(df,qid,lvl,type_inp,lattice,max_gen,dictcatdone):
        if(lvl != 0): #if a generalization is necessary
            if type_inp == 'int':
                if(lvl != max_gen): #not max generalization
                    i = 0
                    rule = json.loads(lattice)[str(max_gen - lvl)] #load the 2D array of integer generalization law
                    tab_rule = []
                    for r in rule: #split string into ranges
                        temp_s = r.split(" ")
                        tab_rule.append([temp_s[1],temp_s[3]]) #append lower and upper limit
                    while(i < len(df)): #foreach value
                        findrule = False
                        for r2 in tab_rule: #test each rule
                            if(int(df.at[i,qid]) >= int(r2[0]) and int(df.at[i,qid]) <= int(r2[1])):
                                df.at[i,qid] = "[ " +  r2[0] + " ; " + r2[1] + " ]"
                                findrule = True
                                break
                        if(not findrule):
                            df.at[i,qid] = "Other"
                        i = i + 1
                else: #max generalization (= '*')
                    i = 0
                    while(i < len(df)): #foreach value
                        df.at[i,qid] = '*'
                        i += 1
            elif type_inp == 'cat':
                if(qid not in dictcatdone.keys()):
                    dictcatdone[qid] = {}
                keys = dictcatdone[qid].keys() #check if previous gen has been done to save time
                min = 0
                for key in keys:
                    if(int(key) > min and int(key) <= lvl):
                        min = int(key)
                if(min != 0):
                    df[qid] = dictcatdone[qid][str(min)]
                while min < lvl:
                    rule = json.loads(str(lattice.replace(";",',').split("|")[min]))
                    keyslvl = list(rule.keys())
                    i = 0
                    while(i < len(df)): #foreach value
                        cmpt = 0
                        for val in rule.values():
                            if(df.at[i,qid] in val):
                                df.at[i,qid] = keyslvl[cmpt]
                                break
                            cmpt += 1
                        i += 1
                    dictcatdone[qid][str(min+1)] = df[qid].copy()
                    min += 1
            else:
                rule = json.loads(lattice)[lvl-1]
                i = 0
                while(i < len(df)): #foreach value
                    cmptpos = 0
                    for r in rule:
                        if(r != 'X'):
                            temp = list(df.at[i,qid])
                            temp[cmptpos] = "*"
                            df.at[i,qid] = ''.join(temp)
                        cmptpos += 1
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
        dictcatdone = {}
        list_comb = SSW.create_lattice(max_gen)
        list_cost = []
        current_level = [math.floor(len(list_comb)/2)] #start of binary search
        stop = False
        while not stop:
            found_no_supp = False
            cost = []
            for c in list_comb[current_level[len(current_level)-1]]: #for all node in lattice's current level
                df = df_init.copy() #create copy to work with it
                for q in range(0,len(qid)): #foreach qid
                    df = SSW.generalize(df,qid[q],c[q],types[q],lattice[q],max_gen[q],dictcatdone) #apply generalization level
                count_supp = 0
                ano = SSW.check_ano(df,qid) #get global k-anonymity
                if(ano < k): 
                    size_class = SSW.get_class(df,qid)
                    for s in size_class: #for all equivalence classes
                        if(s < k): #if class size is less than k
                            count_supp += s #add class size to total suppression count
                    ano = k
                if(count_supp/len(df)*100 <= max_supp): #if suppression rate is OK
                    found_no_supp = True #solution is OK
                sum_w = 0
                for q2 in range(0,len(qid)): #calculate total cost with custom weights
                    sum_w += sum(weigths[q2][0:c[q2]])
                if(found_no_supp):
                    cost.append([df,c,round(count_supp * sum(sum(weigths,[])) + (len(df)-count_supp) * sum_w,2),ano,round(count_supp/len(df)*100,2)]) #cost storage
            if(found_no_supp): #if solution is OK
                if(len(current_level) == 1):
                    current_level.append(math.floor(len(list_comb)/4)) #go to lower generalization level
                else:
                    if(current_level[-2] < current_level[-1]):
                        if(math.floor(abs(current_level[-2] - current_level[-1])/2) != 0):
                            current_level.append(current_level[-1] - math.floor((current_level[-2] - current_level[-1])/2))
                        else:
                            stop = True
                    else:
                        if(math.floor(current_level[-1]/2) != current_level[-1]):
                            current_level.append(math.floor(current_level[-1]/2))
                        else:
                            stop = True                
                list_cost.append(cost)
            else: #solution is not OK
                if(len(current_level) == 1):
                    current_level.append(math.floor(3*len(list_comb)/4))#go to greater generalization level
                else:
                    if(current_level[-2] > current_level[-1]):
                        if(math.floor(abs(current_level[-2] - current_level[-1])/2) != current_level[-1]):
                            current_level.append(math.floor((current_level[-2] - current_level[-1])/2))
                        else:
                            stop = True
                    else:
                        if(current_level[-1] + math.floor((len(list_comb) - current_level[-1])/2) != current_level[-1]):
                            current_level.append(current_level[-1] + math.floor((len(list_comb) - current_level[-1])/2))
                        else:
                            stop = True
        return list_cost