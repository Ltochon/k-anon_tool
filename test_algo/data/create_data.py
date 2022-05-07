import os
from random import randint
import numpy as np
import pandas as pd
#zip = ["1001","1002","1003","1004","1201","1202","1203","1204","01","01","01","02","02","02"]
zip = ["1001","1002","1003","1004","1201","1202","1203","1204"]
cancer_illness = ["Lung cancer","Breast cancer", "Colorectal cancer", "Kidney cancer","Bladder cancer"]
sexual_illness = ["Chlamydia", "HIV","Syphilis", "AIDS"]
illness = cancer_illness + sexual_illness
ill, ill2, ill3 = [],[],[]
age, age2, age3 = [],[],[]
zip_list,canton_list,pays_list = [],[],[]
for x in range(500):
    e = randint(0,len(zip)-1)
    a = randint(10,50)
    i = randint(0,len(illness)-1)
    ill.append(illness[i])
    age.append(a)
    zip_list.append(zip[e])
df = pd.DataFrame()
df["zip"] = zip_list
df["age"] = age
df["illness"] = ill
cwd = os.getcwd()
path = cwd + "/test_algo/data/complete_data_test.csv"
df.to_csv(path)