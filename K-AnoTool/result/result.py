import sys
import json
from operator import itemgetter 
from flask import Blueprint, Response, current_app, render_template
sys.path.append('./')
from test_algo.ssw import algo

result = Blueprint("result", __name__, static_folder="static", template_folder="templates")

@result.route("/")
def result_page():
    data = current_app.config['data']
    inputs = ["level_","checkbox_","type_"]
    tab_level = []
    tab_check = []
    tab_type = []
    for header in data.columns:
        for i in range(0,len(inputs)):
            txt = inputs[i]+header
            if(i == 0):
                tab_level.append(current_app.config[txt]),
            elif(i ==1):
                tab_check.append(current_app.config[txt]),
            else:
                tab_type.append(current_app.config[txt])
    index_qid = [i for i, x in enumerate(tab_check) if x == "on"]

    qid = itemgetter(*index_qid)(data.columns)
    qid_str = []
    for q in qid: #need to transform from 
        qid_str.append(q.replace("'",'"'))
    k = int(current_app.config['inputk'])
    max_supp = int(current_app.config['inputmaxsupp'])
    weights = itemgetter(*index_qid)(tab_level)
    types = itemgetter(*index_qid)(tab_type)
    compute_ano = algo(data,qid_str,[2,2],[[3,4],[5,6]],k,max_supp)
    list_cost = []
    for i in compute_ano:
        for j in i:
            list_cost.append(j[2])
    list_cost.sort()
    if(len(list_cost) < 5):
        lastitem = len(list_cost)
    else:
        lastitem = 5
    df,ano,comb,cost,suppr = [],[],[],[],[]
    for j in compute_ano:
        for i in j:
            for c in list_cost[0:lastitem]:
                if(i[2] == c):
                    df.append(i[0])
                    ano.append(i[3])
                    comb.append(i[1])
                    cost.append(i[2])
                    suppr.append(i[4])
    current_app.config['final_df'] = df
    current_app.config['qid'] = qid
    current_app.config['weights'] = weights
    current_app.config['k'] = str(ano)
    current_app.config['comb'] = str(comb)
    current_app.config['cost'] = str(cost)
    current_app.config['suppr'] = str(suppr)
    return render_template("result.html", df = df, k = ano, comb = comb, cost = cost, suppr = suppr)

    
