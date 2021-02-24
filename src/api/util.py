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
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import io
import matplotlib

matplotlib.use('Agg')
from model_trans import *


"""
Function to create generator from the csv file
input
    csv_path: path to the csv file
    image_path: path to the image directory
    target: the class of interest(age, gender, or race)
    size: the size of the image
    batch_size: the batch size
    preprocess_input: The preprocess function to apply based on different transfer learning model. Make sure to change
    the import statement above if wants to apply different transfer learning model
    mapping_path: a directionary objects indicating how each category is being mapped to the respective integer representation
    is_training: whether or not the generator is used as training

output
    a generator object ready to be trained
"""
def create_generator(csv_path, image_path, target, size, batch_size, mapping_path, preprocess_input, is_training):
    
    if is_training:
        rotation_range = 30
        horizontal_flip = True
        vertical_flip = True
        shuffle = True
    else:
        rotation_range = 0
        horizontal_flip = False
        vertical_flip = False
        shuffle = False
    
    df = pd.read_csv(csv_path)
    df["file"] = df["file"].apply(lambda x: os.path.join(image_path, x.split("/")[1]))
    
    imgdatagen = ImageDataGenerator(
        preprocessing_function = preprocess_input,
        rotation_range = rotation_range,
        horizontal_flip = horizontal_flip, 
        vertical_flip = vertical_flip,
        #rescale = 1.0 / 255
    )
    
    data_generator = imgdatagen.flow_from_dataframe(
        dataframe = df,
        directory = None,
        x_col = "file",
        y_col = target,
        target_size = (size, size),
        batch_size = batch_size,
        save_format = "jpg",
        shuffle = shuffle
    )
    
    with open(mapping_path, "w") as f:
        json.dump(data_generator.class_indices, f)
    f.close()
    
    return data_generator
    

"""
function to visualize the training progress
input
    log_path: The csv file that logged the training progress
    target: the name of the class (e.g. age, race, gender)
output
    the accuray and loss curve for both the training and validation
"""
def generate_curves(log_path, save_path):
    
    if not os.path.exists(save_path):
        os.mkdir(save_path)
       
    df = pd.read_csv(log_path)
    path_to_viz = save_path
    acc_name = os.path.join(path_to_viz, "acc_curve")
    loss_name = os.path.join(path_to_viz, "loss_curve")
    
    ax = plt.gca()
    plt.plot(df["accuracy"])
    plt.plot(df["val_accuracy"])
    plt.title("Training Accuracy vs. Validation Accuracy")
    plt.xlabel("epochs")
    plt.ylabel("Accuracy")
    ax.legend(['Train','Validation'],loc='lower right')
    plt.savefig(acc_name)
    plt.close()
    
    ax = plt.gca()
    plt.plot(df["loss"])
    plt.plot(df["val_loss"])
    plt.title("Training loss vs. Validation loss")
    plt.xlabel("epochs")
    plt.ylabel("Loss")
    ax.legend(['Train','Validation'],loc='upper right')
    plt.savefig(loss_name)
    

"""
Function to evaluate the model by calculating category-specific statistics
input
    model: a loaded model
    generator: a generator that contains data
    label_df: the csv file that contains the information of the data
    target: the name of the class (e.g. age, race, gender)
    target_map: The mapping of the class
    save_path: where the plot should be saved
output
    The class-specific barplot for precision, recall, f1-score, accuracy, and support
"""
def create_stats(model, generator, target, label_path, mapping_path, save_path):
    
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    label_df = pd.read_csv(label_path)
    with open(mapping_path) as f:
        target_map = json.load(f)
    f.close()
    
    pred = model.predict(generator).argmax(axis = 1)
    ground_truth = label_df[target].replace(target_map).values
    cr = classification_report(ground_truth, pred, target_names = target_map.keys())
    
    with open(os.path.join(save_path, "class_report.txt"), "w") as f:
        f.write(cr)
    f.close()
    
    cr = classification_report(ground_truth, pred, target_names = target_map.keys(), output_dict = True)
    
    result_df = pd.DataFrame(cr).T.iloc[:len(target_map), :]
    result_df = result_df.reset_index().rename(columns= {"index": "category"})

    cm = confusion_matrix(ground_truth, pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    acc = cm.diagonal()
    result_df["accuracy"] = acc
    result_df.to_csv(os.path.join(save_path, "result_df.csv"), index = False)

    stat_names = ["precision", "recall", "f1-score", "accuracy", "support"]
    
    for name in stat_names:
        save_dir = os.path.join(save_path, name + "_barplot")
        plt.figure(figsize = (12,8))
        sns.barplot(x = "category", y= name, data= result_df,linewidth=2.5, 
                    facecolor=(1, 1, 1, 0), edgecolor="0")
        plt.title("{} across {}".format(name, target), fontsize = 20)
        plt.xlabel(target, fontsize = 16)
        plt.ylabel(name, fontsize= 16)
        plt.savefig(save_dir)  

"""
function to get the prediction from the model
input
    img_path: The path to the image
    model_path: The path to the model
    mapping_path: The mapping
out
    The prediction made by the model
"""

"""
function to make a single prediction of an image
input
    img_path: The path to the image
    model_path: The path to the model
    mapping_path: The mapping between labels(in number) and categories
    result_df_path: The aggregate results
output
    out: The prediction
    pred_prob: The accuracy of making the out prediction
    aggregate_acc: The accuracy of the aggregate category

***NOTE: result_df_path can be found in(assuming race):
    "./visualization/race/stats/result_df.csv"
"""
def get_prediction(img_path, model_path, mapping_path, result_df_path):
    img_arr = detect_face(img_path)
    if img_arr.shape != (1, 224,224,3):
        print("Wrong input size")
        return
    else:
        model = keras.models.load_model(model_path)
        
        with open(mapping_path) as f:
            mapping = json.load(f)
        f.close()
        mapping = {val:key for key, val in mapping.items()}
        pred = model.predict(img_arr).squeeze()
        out = mapping[pred.argmax()]
        pred_prob = np.round(pred[pred.argmax()] * 100, 4)
        
        result_df = pd.read_csv(result_df_path)
        aggregate_acc = np.round(result_df[result_df["category"] == out]["accuracy"].values[0] * 100, 4)
    
    return out, pred_prob, aggregate_acc

"""
Convert a Matplotlib figure to a PIL Image and return it
"""
def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

"""
functions to load the model with weights

in: weight_name of the checkpoint
out: the model loaded with weights
"""
def load_model_with_weights(weight_name):
    if "age" in weight_name:
        num_classes = 9
    elif "race" in weight_name:
        num_classes = 7
    else:
        num_classes = 2
    
    model = build_model(num_classes = num_classes)
    model.load_weights(weight_name)
    
    return model

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
             

    
