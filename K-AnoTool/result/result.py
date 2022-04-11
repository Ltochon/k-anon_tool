import sys
import json
from operator import itemgetter 
from flask import Blueprint, Response, current_app, render_template
sys.path.append('../')
from test_algo.datafly_v1_weighted import run

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
    weights = itemgetter(*index_qid)(tab_level)
    types = itemgetter(*index_qid)(tab_type)
    compute_ano = run(data,k,qid_str,weights,[1,1])
    current_app.config['final_df'] = compute_ano[0]
    current_app.config['qid'] = qid
    current_app.config['weights'] = weights
    current_app.config['k'] = str(compute_ano[1])
    return render_template("result.html", df = compute_ano[0].head(50), k = compute_ano[1])

    
