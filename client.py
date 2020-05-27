from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
import json
import cv2
import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__)
UPLOAD_FOLDER = '/home/BaksoKuah20K/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
addr = 'http://MieAyamBakso20K.pythonanywhere.com'
test_url = addr + '/api/test'

@app.route('/')
def home():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      # prepare headers for http request
      content_type = 'image/jpeg'
      headers = {'content-type': content_type}

      img = cv2.imread(filename)
      # encode image as jpeg
      _, img_encoded = cv2.imencode('.jpg', img)
      # send http request with image and receive response
      response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
      return json.loads(response.text)
      # decode response
