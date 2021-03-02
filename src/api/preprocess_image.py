import pandas as pd
import os
from PIL import Image
import dlib
import numpy as np
import os
import sys
from tensorflow.keras.applications import resnet_v2
IM_WIDTH = IM_HEIGHT = 198

def rect_to_bb(rect):
	# take a bounding predicted by dlib and convert it
	# to the format (x, y, w, h) as we would normally do
	# with OpenCV
	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y
	# return a tuple of (x, y, w, h)
	return (x, y, w, h)

def detect_face(img, default_max_size=800,size = 224, padding = 0.25):
    cnn_face_detector = dlib.cnn_face_detection_model_v1('models/mmod_human_face_detector.dat')
    sp = dlib.shape_predictor('models/shape_predictor_5_face_landmarks.dat')
    base = 2000  # largest width and height

    # img = dlib.load_rgb_image(image_path)
    # im = Image.fromarray(img, 'RGB')
    # im.save("test.jpeg")
    old_height, old_width, _ = img.shape
    old_height, old_width, _ = img.shape

    if old_width > old_height:
        new_width, new_height = default_max_size, int(default_max_size * old_height / old_width)
    else:
        new_width, new_height =  int(default_max_size * old_width / old_height), default_max_size
    img = dlib.resize_image(img, rows=new_height, cols=new_width)
    dets = cnn_face_detector(img, 1)
    num_faces = len(dets)
    if num_faces == 0:
        print("Sorry, there were no faces found in '{}'".format(image_path))
        return
    elif num_faces > 1:
        print("Multiple face in '{}'. A random face will be returned".format(image_path))
    faces = dlib.full_object_detections()
    for detection in dets:
        rect = detection.rect
        faces.append(sp(img, rect))
    image = dlib.get_face_chips(img, faces, size=size, padding = padding)[0]

    image = Image.fromarray(image, 'RGB')

    return image

# from PIL import Image
# import cv2 
# import numpy as np

# def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
#     # initialize the dimensions of the image to be resized and
#     # grab the image size
#     dim = None
#     (h, w) = image.shape[:2]

#     # if both the width and height are None, then return the
#     # original image
#     if width is None and height is None:
#         return image

#     # check to see if the width is None
#     if width is None:
#         # calculate the ratio of the height and construct the
#         # dimensions
#         r = height / float(h)
#         dim = (int(w * r), height)

#     # otherwise, the height is None
#     else:
#         # calculate the ratio of the width and construct the
#         # dimensions
#         r = width / float(w)
#         dim = (width, int(h * r))

#     # resize the image
#     resized = cv2.resize(image, dim, interpolation = inter)

#     # return the resized image
#     return resized

# def detect_face(image):
#     image = image_resize(image, height = 800)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     faces = faceCascade.detectMultiScale(
#         gray,
#         scaleFactor=1.3,
#         minNeighbors=1,
#         minSize=(224, 224)
#     )
#     print("[INFO] Found {0} Faces!".format(len(faces)))
#     for (x, y, w, h) in faces[:1]:
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         roi_color = image[y:y + h, x:x + w]
#         print("[INFO] Object found.")
#     img = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)
#     im_pil = Image.fromarray(img, 'RGB')

#     return im_pil