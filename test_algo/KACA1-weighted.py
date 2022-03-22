from operator import index, itemgetter
import pandas as pd

def read_file(path, delim):
    csv = pd.read_csv(path, sep=delim)
    return csv

def check_ano(df,qid):
    datas_qid = df[qid]
    dups_shape = datas_qid.pivot_table(columns=qid, aggfunc='size')
    return min(dups_shape)

def WHD(p,q,wh): #Weighted Hierarchical Distance
    if(p <= q): return False
    up_sum = 0
    down_sum = sum(wh)
    for i in range (1,p-q+1):
        up_sum += wh[p-i-1]
    return up_sum/down_sum

print(__file__)
df = read_file('k-ano_Tool/test_algo/data/adult.csv', ';')
k = 4
qid = ["10","13"]
wh = [4]
print(WHD(2,1,wh))
