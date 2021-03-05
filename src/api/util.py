import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.layers import Activation, Dropout, Lambda, Dense
from tensorflow.keras import Sequential
from IntegratedGradients import *
import json
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from tensorflow.keras.applications import resnet_v2
import seaborn as sns
import matplotlib.pyplot as plt
import io
import matplotlib
from grad_cam import *

matplotlib.use('Agg')
from model_trans import *

def grad_cam(PIL_img, target, lookup = None, to_save = False):
    #loading models and params
    if target == "race":
        model_path = "models/race_v6.hdf5"
        mapping_dict_rev = {0: 'Black', 1: 'East Asian', 2: 'Latino/Hispanic', 3: 'Indian', 4: 'Middle Eastern', 5: 'SE Asian', 6: 'White'}
    elif target == "age":
        model_path = "models/age_v1.hdf5"
        mapping_dict_rev = {0: "0-2", 1: "10-19", 2: "20-29", 3: "3-9", 4: "30-39", 5: "40-49", 6: "50-59", 7: "60-69", 8: "more than 70"}
    else:
        model_path = "models/gender_v1.hdf5"
        mapping_dict_rev = {0: "Female", 1: "Male"}
    
    model = keras.models.load_model(model_path)
    nb_classes = model.output.shape[1]
    
    # #read the mapping
    # mapping = os.path.join("./mapping", target + ".json")
    # with open(mapping) as f:
    #     mapping_dict = json.load(f)
    # f.close()
    
    # mapping_dict = {key.lower():val for key, val in mapping_dict.items()}
    # mapping_dict_rev = {val:key for key, val in mapping_dict.items()}
    
    
    #preprocess image
    PIL_img = np.array(PIL_img).astype("float32")[None, :]
    image = resnet_v2.preprocess_input(PIL_img)
    preprocessed_input = image
    
    #inference 
    if lookup == None:
        output_prob = model.predict(image).squeeze()
        pred_idx = output_prob.argmax()
    else:
        lookup = lookup.lower()
        pred_idx = mapping_dict[lookup]
    
    #grad_cam
    target_layer = lambda x: target_category_loss(x, pred_idx, nb_classes)
    model.add(Lambda(target_layer,
                     output_shape = target_category_loss_output_shape))

    loss = K.sum(model.layers[-1].output)
    conv_output =  [l for l in model.layers if l.name == "conv2d_7"][0].output
    grads = normalize(K.gradients(loss, conv_output)[0])
    gradient_function = K.function([model.layers[0].input], [conv_output, grads])

    output, grads_val = gradient_function([image])
    output, grads_val = output[0, :], grads_val[0, :, :, :]

    weights = np.mean(grads_val, axis = (0, 1))
    cam = np.ones(output.shape[0 : 2], dtype = np.float32)

    for i, w in enumerate(weights):
        cam += w * output[:, :, i]

    cam = cv2.resize(cam, (224, 224))
    cam = np.maximum(cam, 0)
    heatmap = cam / np.max(cam)

    #Return to BGR [0..255] from the preprocessed image
    image = image[0, :]
    image -= np.min(image)
    image = np.minimum(image, 255)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

    cam = cv2.applyColorMap(np.uint8(255*heatmap), cv2.COLORMAP_RAINBOW)
    cam = np.float32(cam / 255) + np.float32(image)
    cam = 255 * cam / np.max(cam)
    cam = np.uint8(cam)
    
    register_gradient()
    guided_model = modify_backprop(model, 'GuidedBackProp', model_path)
    saliency_fn = compile_saliency_function(guided_model)
    saliency = saliency_fn([preprocessed_input, 0])
    gradcam = saliency[0] * heatmap[..., np.newaxis]
    guided = deprocess_image(gradcam)
 
    cam = Image.fromarray(cam)
    guided = Image.fromarray(guided)
    
    
    # if to_save:
    #     cam.save("./grad_cam.png")
    #     guided.save("./guided_cam.png")
        
    return cam, guided


"""
grad_cam function that converts a PIL image to NORMALIZED grad_cam heatmap
input 
    PIL_img: a PIL_img object PIL.Image.Image
    
    target: the target(e.g. race, age, gender)
    
    lookup: The particular category to lookup. For instance, given target = race, lookup = None
            would display the heatmap with the highest probability. But if lookup = "white",
            the function would display the heatmap with "white" category even if the category
            does have have the highest probability.
    
    to_save: Whether or not to save the heatmap. If true, the heatmaps wil be saved in the current directory.
   
output
     two image of object PIL.PngImagePlugin.PngImageFile: normalized grad_cam from unbiased and biased model
"""
def grad_cam_normalized(PIL_img, target, lookup = None, to_save = False):
    
    #loading models and params
    if target == "race":
        model_path = "./models/race/race_v6.hdf5"
        model_path_biased = "./models/race/race_biased_v1.hdf5"
    elif target == "age":
        model_path = "./models/age/age_v1.hdf5"
        model_path_biased = "./models/age/age_biased_v1.hdf5"
    else:
        model_path = "./models/gender/gender_v6.hdf5"
        model_path_biased = "./models/gender/gender_biased_v1.hdf5"
        
    model = keras.models.load_model(model_path)
    biased_model = load_model(model_path_biased)

    nb_classes = model.output.shape[1]
    
    #read the mapping
    mapping = os.path.join("./mapping", target + ".json")
    with open(mapping) as f:
        mapping_dict = json.load(f)
    f.close()
    
    mapping_dict = {key.lower():val for key, val in mapping_dict.items()}
    mapping_dict_rev = {val:key for key, val in mapping_dict.items()}
    
    
    #preprocess image
    PIL_img = np.array(PIL_img).astype("float32")[None, :]
    image = resnet_v2.preprocess_input(PIL_img)
    preprocessed_input = image
    
    #inference 
    if lookup == None:
        output_prob = model.predict(image).squeeze()
        output_prob_biased = biased_model.predict(image).squeeze()
        pred_idx = output_prob.argmax()
        pred_idx_biased = output_prob_biased.argmax()
    else:
        lookup = lookup.lower()
        pred_idx = mapping_dict[lookup]
        pred_idx_biased = mapping_dict[lookup]
        
    
    #grad_cam
    target_layer = lambda x: target_category_loss(x, pred_idx, nb_classes)
    biased_target_layer = lambda x: target_category_loss(x, pred_idx_biased, nb_classes)
    
    model.add(Lambda(target_layer,
                     output_shape = target_category_loss_output_shape))
    
    biased_model.add(Lambda(biased_target_layer,
                     output_shape = target_category_loss_output_shape))

    loss = K.sum(model.layers[-1].output)
    biased_loss = K.sum(biased_model.layers[-1].output)
    
    conv_output =  [l for l in model.layers if l.name == "conv2d_7"][0].output
    biased_conv_output =  [l for l in biased_model.layers if l.name == "conv2d_7"][0].output
    
    
    grads = normalize(K.gradients(loss, conv_output)[0])
    biased_grads = normalize(K.gradients(biased_loss, biased_conv_output)[0])
    
    gradient_function = K.function([model.layers[0].input], [conv_output, grads])
    biased_gradient_function = K.function([biased_model.layers[0].input], [biased_conv_output, biased_grads])
    

    output, grads_val = gradient_function([image])
    biased_output, biased_grads_val = biased_gradient_function([image])
    
    output, grads_val = output[0, :], grads_val[0, :, :, :]
    biased_output, biased_grads_val = biased_output[0, :], biased_grads_val[0, :, :, :]
    

    weights = np.mean(grads_val, axis = (0, 1))
    biased_weights = np.mean(biased_grads_val, axis = (0, 1))
    
    cam = np.ones(output.shape[0 : 2], dtype = np.float32)
    biased_cam = np.ones(biased_output.shape[0 : 2], dtype = np.float32)

    for i, w in enumerate(weights):
        cam += w * output[:, :, i]
    for i, w in enumerate(biased_weights):
        biased_cam += w * biased_output[:, :, i]

    cam = cv2.resize(cam, (224, 224))
    biased_cam = cv2.resize(biased_cam, (224, 224))
    cam = np.maximum(cam, 0)
    biased_cam = np.maximum(biased_cam, 0)

    max_arr = np.concatenate([cam,biased_cam])
    max_norm = np.max(max_arr)

    heatmap = cam / max_norm
    biased_heatmap = biased_cam/ max_norm
    
    #Return to BGR [0..255] from the preprocessed image
    image = image[0, :]
    image -= np.min(image)
    image = np.minimum(image, 255)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    cam = cv2.applyColorMap(np.uint8(255*heatmap), cv2.COLORMAP_JET)
    biased_cam = cv2.applyColorMap(np.uint8(255*biased_heatmap), cv2.COLORMAP_JET)

    cam = np.float32(cam / 255) + np.float32(image)
    biased_cam = np.float32(biased_cam / 255) + np.float32(image)
    
    cam = 255 * cam / np.max(cam)
    biased_cam = 255 * biased_cam / np.max(biased_cam)
    
    cam = np.uint8(cam)
    biased_cam = np.uint8(biased_cam)
    
    cam = Image.fromarray(cam)
    biased_cam = Image.fromarray(biased_cam)
    
    return cam, biased_cam

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

"""
Another version of integrated_grad implementation that just shows the heatmap with the highest
predictive accuracy

NOTE: Before running this, Make sure you:
    1. Called Detect_face to crop the image only(WITHOUT USING Resnet Preprocessing)
    2. You should call resnet preprocessing unit INSIDE this function because
       the PIL.fromarray CANNOT take in float32 data type
       
   ALSO: Make sure you'd changed the model path and mapping path so that the function can run.

in: 
    PIL_img: a PIL_img object PIL.Image.Image
    
    target: the target(e.g. race, age, gender)
    
    lookup: The particular category to lookup. For instance, given target = race, lookup = None
            would display the heatmap with the highest probability. But if lookup = "white",
            the function would display the heatmap with "white" category even if the category
            does have have the highest probability.
   
out:
    a single image of object PIL.PngImagePlugin.PngImageFile
"""
def integrated_grad_PIL(PIL_img, target, lookup = None):
    if target == "race":
        model_path = "models/race_v6.hdf5"
        mapping_dict_rev = {0: 'Black', 1: 'East Asian', 2: 'Latino/Hispanic', 3: 'Indian', 4: 'Middle Eastern', 5: 'SE Asian', 6: 'White'}
    elif target == "age":
        model_path = "models/age_v1.hdf5"
        mapping_dict_rev = {0: "0-2", 1: "10-19", 2: "20-29", 3: "3-9", 4: "30-39", 5: "40-49", 6: "50-59", 7: "60-69", 8: "more than 70"}
    else:
        model_path = "models/gender_v1.hdf5"
        mapping_dict_rev = {0: "Female", 1: "Male"}

    mapping_dict = {v: k for k, v in mapping_dict_rev.items()}
    model = keras.models.load_model(model_path)
    ig = integrated_gradients(model)

    # mapping = os.path.join("./mapping", target + ".json")
    # with open(mapping) as f:
    #     mapping_dict = json.load(f)
    # f.close()

    # mapping_dict = {key.lower():val for key, val in mapping_dict.items()}
    # mapping_dict_rev = {val:key for key, val in mapping_dict.items()}

    ############################THIS LINE IS IMPORTANT!!!!#################################
    PIL_img = resnet_v2.preprocess_input(np.array(PIL_img)[None,:]) ##IMPORTANT!!!
    output_prob = model.predict(PIL_img).squeeze()
    pred_idx = output_prob.argmax()
    
    if lookup == None:
        pass
    else:
        lookup = lookup.lower()
        pred_idx = mapping_dict[lookup]

    ex = ig.explain(PIL_img.squeeze(), outc=pred_idx)

    th = max(np.abs(np.min(ex)), np.abs(np.max(ex)))

    plt.figure(figsize = (6, 6))
    plt.imshow(ex[:,:,0], cmap="seismic", vmin=-1*th, vmax=th)
    plt.title("heatmap for {} {} with probability {:.2f}".format(target, mapping_dict_rev[pred_idx],
                                                                 output_prob[pred_idx]), fontsize=12)
    
    fig = plt.gcf()
    im = fig2img(fig)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    return im
             

    
