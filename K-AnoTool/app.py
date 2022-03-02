import csv
from datetime import timedelta
import os
from numpy import save
import pandas as pd
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
from upload.upload import upload

app = Flask(__name__)
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
          # save the file
      return redirect(url_for('csv'))

if (__name__ == "__main__"):
     app.run(port = 5000)