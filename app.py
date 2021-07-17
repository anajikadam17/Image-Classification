import os
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image

from tensorflow import keras

import numpy as np
import cv2
import PIL.Image as Image
import os


json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")


model_path = r"flower_CNN_TL_model"
model1 = keras.models.load_model(model_path)
print("Loaded models from disk")


def classify(img_file):
    img_name = img_file
    test_image = image.load_img(img_name, target_size = (64, 64))

    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)

    if result[0][0] == 1:
        prediction = 'Orange'
    else:
        prediction = 'Apple'
    print(prediction,img_name)
    return prediction

def classify1(file_path):
    flowers_labels_dict = {
        'roses': 0,
        'daisy': 1,
        'dandelion': 2,
        'sunflowers': 3,
        'tulips': 4,
    }
    def readImg(path):
      img = cv2.imread(str(path))
      resized_img = cv2.resize(img,(224,224))
      xtest = np.array([resized_img])
      xtest_scaled = xtest / 255
      return xtest_scaled
      
    def getKey(dct,value):
      return [key for key in dct if (dct[key] == value)][0]

    xtest_scaled = readImg(file_path)

    pred = model1.predict(xtest_scaled)
    pred = np.argmax(pred, axis=1)[0]

    prediction = getKey(flowers_labels_dict, pred)
    print("Flower name is ",prediction)
    return prediction

basepath = r'D:\PythonPC\AI Master Class\Day12'

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        preds = classify(file_path)
        return preds
    return None

@app.route('/index1', methods=['GET'])
def index1():
    # index1 Main page
    return render_template('index1.html')
    
@app.route('/project1', methods=['GET', 'POST'])
def project1():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file1']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        preds = classify1(file_path)
        return preds
    return None

if __name__ == '__main__':
    app.run(debug=True)

