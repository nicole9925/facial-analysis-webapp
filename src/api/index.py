from flask import json, Flask, render_template, make_response, send_file, request, redirect, flash, url_for, Response, jsonify
import urllib.request
from werkzeug.utils import secure_filename
# from app import app
import os
import sys
from PIL import Image
import base64
from io import BytesIO
import shutil
from preprocess_image import detect_face
from io import BytesIO
from keras.models import load_model
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet_v2 import preprocess_input
import cv2
from werkzeug.exceptions import HTTPException
from util import *

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
GEN_FOLDER = 'static/generated_images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/', methods=['GET', 'POST'])
# def index(): 
#     return render_template('index.html')

@app.route('/api/clear/')
def clear():

    path =  os.path.join(os.getcwd(), UPLOAD_FOLDER)
    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(UPLOAD_FOLDER)

    path =  os.path.join(os.getcwd(), GEN_FOLDER)
    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(GEN_FOLDER)

    return "Made directory"

@app.route('/api/upload/', methods=['POST'])
def fileUpload():
    # Decode and save original file
    global name 
    name = secure_filename(request.form.get('filename'))
    filename = os.path.join(UPLOAD_FOLDER, name)

    image_data = bytes(request.form.get('file'), encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')
    im.save(filename)

    # Preprocess image, make predictions
    _, image_encoded, image = preprocess(filename)
    race, gender, age, race_results, gender_results, age_results = predict(image)
    race_ig, gender_ig, age_ig = generate_integrated_grad(image)

    # Formulate Response
    data = {"pp_img": image_encoded, 
            "race": race,
            "gender": gender,
            "age": age,
            "race_results": race_results,
            "gender_results": gender_results,
            "age_results": age_results, 
            "race_ig": race_ig,
            "gender_ig": gender_ig,
            "age_ig": age_ig
            }
    resp = app.response_class(
    status=200,
    response= json.dumps(data),
    mimetype='application/json'
        )
    return resp

def preprocess(file_path):
    gen_path = os.path.join(GEN_FOLDER, name)

    #Crop face
    image = detect_face(file_path)
    image.save(gen_path)

    img_str = encode_image(image)

    return gen_path, img_str, image

def predict(image):
    resized = preprocess_input(cv2.resize(np.array(image), (224, 224)).reshape(-1, 224, 224, 3))

    # Race
    race_dict = {0: 'Black', 1: 'East Asian', 2: 'Latino/Hispanic', 3: 'Indian', 4: 'Middle Eastern', 5: 'SE Asian', 6: 'White'}
    race_model = load_model('models/race_v6.hdf5')
    race_pred = race_model.predict(resized)
    race = race_dict[np.argmax(race_pred)]

    race_percent = list(map(lambda x: round(x*100),race_pred[0]))
    race_results = []
    for i in range(len(race_percent)):
        race_results.append({"cat": race_dict[i], "val": race_percent[i]})



    # Gender
    gender_dict = {0: "Female", 1: "Male"}
    gender_model = load_model('models/gender_v1.hdf5')
    gender_pred = gender_model.predict(resized)
    gender = gender_dict[np.argmax(gender_pred)]

    gender_percent = list(map(lambda x: round(x*100), gender_pred[0]))
    gender_results = []
    for i in range(len(gender_percent)):
        gender_results.append({"cat": gender_dict[i], "val": gender_percent[i]})


    # Age
    age_dict = {0: "0-2", 1: "10-19", 2: "20-29", 3: "3-9", 4: "30-39", 5: "40-49", 6: "50-59", 7: "60-69", 8: "more than 70"}
    age_model = load_model('models/age_v1.hdf5')
    age_pred = age_model.predict(resized)
    age = age_dict[np.argmax(age_pred)]

    age_percent = list(map(lambda x: round(x*100), age_pred[0]))
    age_results = []
    for i in range(len(age_percent)):
        age_results.append({"cat": age_dict[i], "val": age_percent[i]})
 

    return race, gender, age, race_results, gender_results, age_results

def generate_integrated_grad(image):
    race = encode_image(integrated_grad_PIL(image, "race"))
    gender = encode_image(integrated_grad_PIL(image, "gender"))
    age = encode_image(integrated_grad_PIL(image, "age"))
    return race, gender, age

def encode_image(image):
    """
    Encodes image to be sent to client-side
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('ASCII')
    return img_str


if __name__ == "__main__":
    app.run(debug=True)
