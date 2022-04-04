import os
from random import randint
import numpy as np
import pandas as pd
zip = ["1001","1002","1003","1004","1201","1202","1203","1204","01","01","01","02","02","02"]
zip_list,canton_list,pays_list = [],[],[]
for x in range(200):
    e = randint(0,len(zip)-1)
    zip_list.append(zip[e])
    if(int(zip[e]) < 2):
        canton = "Ain"
        pays = "FR"
    elif(int(zip[e]) < 3):
        canton = "Aisne"
        pays = "FR"
    elif(int(zip[e]) < 1200):
        canton = "VD"
        pays = "CH"
    else:
        canton = "GE"
        pays = "CH"
    canton_list.append(canton)
    pays_list.append(pays)
df = pd.DataFrame()
df["zip"] = zip_list
df["canton"] = canton_list
df["pays"] = pays_list
cwd = os.getcwd()
path = cwd + "/test_algo/data/complete_data_test.csv"
df.to_csv(path)