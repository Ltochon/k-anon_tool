from flask import Blueprint, render_template

upload = Blueprint("upload", __name__, static_folder="static", template_folder="templates")

@upload.route("/")
def upload_page():
    return render_template("upload.html")