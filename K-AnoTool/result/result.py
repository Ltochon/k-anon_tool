from dataclasses import dataclass
import sys
from flask import Blueprint, current_app, render_template

result = Blueprint("result", __name__, static_folder="static", template_folder="templates")

@result.route("/")
def result_page():
    data = current_app.config['data']
    inputs = ["level_","checkbox_","type_"]
    data_details = []
    for header in data.columns:
        for input in inputs:
            txt = input+header
            data_details.append(current_app.config[txt])
    return render_template("result.html", data = data, details = data_details)