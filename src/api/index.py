from flask import json, Flask, render_template, make_response, send_file, request, redirect, flash, url_for, Response, jsonify
import urllib.request
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.resnet_v2 import preprocess_input
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
import cv2
from werkzeug.exceptions import HTTPException
from util import *
import numpy as np

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

    # path =  os.path.join(os.getcwd(), UPLOAD_FOLDER)
    # if os.path.exists(path):
    #     shutil.rmtree(path)

    # os.mkdir(UPLOAD_FOLDER)

    # path =  os.path.join(os.getcwd(), GEN_FOLDER)
    # if os.path.exists(path):
    #     shutil.rmtree(path)

    # os.mkdir(GEN_FOLDER)

    return "Made directory"

@app.route('/api/upload/', methods=['POST'])
def fileUpload():
    # Decode and save original file
    global name 
    name = secure_filename(request.form.get('filename'))
    filename = os.path.join(UPLOAD_FOLDER, name)

    image_data = bytes(request.form.get('file'), encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')
    im_array = np.array(im) 
    # open_cv_image = im_array[:, :, ::-1].copy()
    # Preprocess image, make predictions
    _, image_encoded, image = preprocess(im_array)
    race, gender, age, race_results, gender_results, age_results = predict(image)
    race_grad, race_back, gender_grad, gender_back, age_grad, age_back = generate_grad(image)
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
            "age_ig": age_ig,
            "race_grad": race_grad, 
            "race_back": race_back, 
            "gender_grad": gender_grad, 
            "gender_back": gender_back,
            "age_grad": age_grad, 
            "age_back": age_back
            }
    with open('image.json', 'w') as outfile:
        json.dump(data, outfile)
    resp = app.response_class(
    status=200,
    response= json.dumps(data),
    mimetype='application/json'
        )
    resp.headers.add("Access-Control-Allow-Origin", "*")
    return resp

def preprocess(img_arr):
    gen_path = os.path.join(GEN_FOLDER, name)

    #Crop face
    image = detect_face(img_arr)

    img_str = encode_image(image)
    # print(img_str, file=sys.stderr)
    return gen_path, img_str, image

def predict(input_image):
    arr = np.array(input_image)
    # print(preprocess_input(arr), file=sys.stderr)
    image = preprocess_input(arr[None,:])
    # image = preprocess_input(cv2.resize(arr,(224,224))).reshape(-1, 224, 224, 3)
    # Race
    race_dict = {0: 'Black', 1: 'East Asian', 2: 'Latino/Hispanic', 3: 'Indian', 4: 'Middle Eastern', 5: 'SE Asian', 6: 'White'}
    race_model = load_model('models/race_v6.hdf5')
    race_pred = race_model.predict(image)
    race = race_dict[np.argmax(race_pred)]

    race_percent = list(map(lambda x: round(x*100),race_pred[0]))
    race_results = []
    for i in range(len(race_percent)):
        race_results.append({"cat": race_dict[i], "val": race_percent[i]})



    # Gender
    gender_dict = {0: "Female", 1: "Male"}
    gender_model = load_model('models/gender_v1.hdf5')
    gender_pred = gender_model.predict(image)
    gender = gender_dict[np.argmax(gender_pred)]

    gender_percent = list(map(lambda x: round(x*100), gender_pred[0]))
    gender_results = []
    for i in range(len(gender_percent)):
        gender_results.append({"cat": gender_dict[i], "val": gender_percent[i]})


    # Age
    age_dict = {0: "0-2", 1: "10-19", 2: "20-29", 3: "3-9", 4: "30-39", 5: "40-49", 6: "50-59", 7: "60-69", 8: "more than 70"}
    age_model = load_model('models/age_v1.hdf5')
    age_pred = age_model.predict(image)
    age = age_dict[np.argmax(age_pred)]

    age_percent = list(map(lambda x: round(x*100), age_pred[0]))
    age_results = []
    for i in range(len(age_percent)):
        age_results.append({"cat": age_dict[i], "val": age_percent[i]})
 

    return race, gender, age, race_results, gender_results, age_results

def generate_integrated_grad(image):
    # arr = np.array(input_image)
    # image = preprocess_input(cv2.resize(arr,(224,224)))
    race = encode_image(integrated_grad_PIL(image, "race"))
    gender = encode_image(integrated_grad_PIL(image, "gender"))
    age = encode_image(integrated_grad_PIL(image, "age"))
    return race, gender, age

def generate_grad(image):
    # arr = np.array(input_image)
    # image = preprocess_input(cv2.resize(arr,(224,224)))
    race_grad, race_back = grad_cam(image, "race")
    print("Race Grad-CAM - Done!", file=sys.stderr)
    gender_grad, gender_back = grad_cam(image, "gender")
    print("Gender Grad-CAM - Done!", file=sys.stderr)
    age_grad, age_back = grad_cam(image, "age")
    print("Age Grad-CAM - Done!", file=sys.stderr)
    race_grad = encode_image(race_grad)
    race_back = encode_image(race_back)
    gender_grad = encode_image(gender_grad)
    gender_back = encode_image(gender_back)
    age_grad = encode_image(age_grad)
    age_back = encode_image(age_back)
    return race_grad, race_back, gender_grad, gender_back, age_grad, age_back

def encode_image(image):
    """
    Encodes image to be sent to client-side
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('ASCII')

    return img_str


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
