from flask import Blueprint, current_app, render_template

generalization = Blueprint("generalization", __name__, static_folder="static", template_folder="templates")

@generalization.route("/")
def generalization_page():
    return render_template("generalization.html")