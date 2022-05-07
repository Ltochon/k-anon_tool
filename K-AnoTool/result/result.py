import sys
from operator import itemgetter 
from flask import Blueprint, Response, current_app, flash, redirect, render_template, jsonify, url_for
sys.path.append('./')
from test_algo.ssw import algo
from test_algo.ssw_web import algo_web

result = Blueprint("result", __name__, static_folder="static", template_folder="templates")

@result.route("/")
def result_page():
    data = current_app.config['data']
    dictotallattsalgo = current_app.config['dictotallattsalgo'] 
    dictotalweightsalgo = current_app.config['dictotalweightsalgo']
    dictotaldepthsalgo = current_app.config['dictotaldepthsalgo']
    inputs = ["checkbox_","type_"]
    tab_check = [] 
    tab_type = []
    tab_weight = []
    tab_lattice = []
    tab_depth = []
    for header in data.columns:
        for i in range(0,len(inputs)):
            txt = inputs[i]+header
            if(i == 0):
                tab_check.append(current_app.config[txt]),
            else:
                tab_type.append(current_app.config[txt])
    index_qid = [i for i, x in enumerate(tab_check) if x == "on"]
    if(len(index_qid) >= 1):
        qid = itemgetter(*index_qid)(data.columns)
        if(isinstance(qid, str)):
            qid = (qid,)
        for q_elem in qid:
            tab_weight.append(list(map(int, dictotalweightsalgo[q_elem].split(','))))
            tab_lattice.append(dictotallattsalgo[q_elem])
            tab_depth.append(int(dictotaldepthsalgo[q_elem])+1)

        qid_str = []
        for q in qid: #need to transform from 
            qid_str.append(q.replace("'",'"'))
        k = int(current_app.config['inputk'])
        max_supp = int(current_app.config['inputmaxsupp'])
        types = itemgetter(*index_qid)(tab_type)
        if(isinstance(types, str)):
            types = (types,)
        #print(types,sys.stderr)
        print(tab_depth,sys.stderr)
        #print(tab_lattice,sys.stderr)
        print(tab_weight,sys.stderr)
        compute_ano = algo_web(data,qid_str,tab_depth,tab_weight,k,max_supp,types,tab_lattice)
        list_cost = []
        for i in compute_ano:
            for j in i:
                list_cost.append(j[2])
        list_cost.sort()
        if(len(list_cost) < 5):
            lastitem = len(list_cost)
        else:
            lastitem = 5
        df,dfjson,ano,comb,cost,suppr = [],[],[],[],[],[]
        for c in list_cost[0:lastitem]:
            for j in compute_ano:
                for i in j:
                    if(i[2] == c):
                        df.append(i[0])
                        dfjson.append(i[0].to_json(orient='records'))
                        ano.append(i[3])
                        comb.append(i[1])
                        cost.append(i[2])
                        suppr.append(i[4])
        current_app.config['final_df'] = df
        current_app.config['qid'] = qid
        current_app.config['k'] = str(ano)
        current_app.config['comb'] = str(comb)
        current_app.config['cost'] = str(cost)
        current_app.config['suppr'] = str(suppr)
        if(len(df) > 0):
            return render_template("result.html", df = df[0], qid = qid, dfjson = dfjson, k = ano, comb = comb, cost = cost, suppr = suppr)
        else:
            return render_template("noresult.html")
    else:
        flash("Select at least one QID")
        return redirect(url_for('upload.upload_page'))
    
