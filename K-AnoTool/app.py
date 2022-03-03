import csv
from datetime import timedelta
import os
import sys
from numpy import save
import pandas as pd
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
from upload.upload import upload

app = Flask(__name__)
app.register_blueprint(upload, url_prefix = "/upload")
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
    data = pd.read_csv(path)
    return render_template('upload.html', tables=[data.to_html(classes='data', header="true")])

if (__name__ == "__main__"):
     app.run(port = 5000)