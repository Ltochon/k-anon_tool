import json
from flask import Blueprint, current_app, render_template

generalization = Blueprint("generalization", __name__, static_folder="static", template_folder="templates")

@generalization.route("/")
def generalization_page():
    dic = {}
    data = current_app.config['data'].head(2)
    for q in data.columns:
        dic[q] = current_app.config["occu_"+q]
    return render_template("generalization.html", dic = json.dumps(dic))