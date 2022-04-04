import os
from random import randint
import numpy as np
import pandas as pd
zip = ["1001","1002","1003","1004","1201","1202","1203","1204","01","01","01","02","02","02"]
age, age2, age3 = [],[],[]
zip_list,canton_list,pays_list = [],[],[]
for x in range(200):
    e = randint(0,len(zip)-1)
    a = randint(10,50)
    age.append(a)
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
    if(a < 20):
        age2.append("<20")
        age3.append("<30")
    elif(a < 30):
        age2.append("<30")
        age3.append("<30")
    elif(a < 40):
        age2.append("<40")
        age3.append(">=40")
    else:
        age2.append(">=40")
        age3.append(">=40")
    
    canton_list.append(canton)
    pays_list.append(pays)
df = pd.DataFrame()
df["zip"] = zip_list
df["canton"] = canton_list
df["pays"] = pays_list
df["age"] = age
df["age_dizaine"] = age2
df["age_split"] = age3
cwd = os.getcwd()
path = cwd + "/test_algo/data/complete_data_test.csv"
df.to_csv(path)