from flask import Blueprint, current_app, render_template

about = Blueprint("about", __name__, static_folder="static", template_folder="templates")

@about.route("/")
def about_page():
    return render_template("about.html")