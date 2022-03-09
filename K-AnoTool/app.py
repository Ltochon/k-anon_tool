import csv
from datetime import timedelta
import os
import sys
from numpy import save
import pandas as pd
from flask import Flask, current_app, redirect, render_template, request, send_from_directory, url_for, flash
from upload.upload import upload
from result.result import result


app = Flask(__name__)
app.register_blueprint(upload, url_prefix = "/upload")
app.register_blueprint(result, url_prefix = "/result")
app.secret_key = "super key"
app.permanent_session_lifetime = timedelta(days=365)
# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\csv.html'
    return render_template('csv.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
          basedir = os.path.abspath(os.path.dirname(__file__))
          file_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], uploaded_file.filename).replace("\\","/")
          # set the file path
          uploaded_file.save(file_path)
          print_csv(file_path)
          # save the file
      return print_csv(file_path)


def print_csv(path):
    data = pd.read_csv(path, sep=request.form['input_delim'], encoding="ISO-8859-1")
    return render_upload(data)

def render_upload(data):
    app.config['data'] = data
    return redirect(url_for('upload.upload_page'))

@app.route("/upload/", methods=['POST'])
def render_result():
    data = current_app.config['data']
    inputs = ["level_","checkbox_","type_"]
    for header in data.columns:
        for input in inputs:
            txt = input+header
            app.config[txt] = request.form.get(txt)
    return redirect(url_for("result.result_page"))

if (__name__ == "__main__"):
    print(app.url_map, sys.stderr)
    app.run(port = 5000)