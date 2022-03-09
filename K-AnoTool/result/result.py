from flask import Blueprint, render_template

result = Blueprint("result", __name__, static_folder="static", template_folder="templates")

@result.route("/")
def result_page():
    return render_template("result.html")