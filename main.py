# -*- coding: utf-8 -*-

"""
Created: 19 March 2022
@author: Ram Sankar (github.com/rrsankar)
"""

import pickle

import numpy as np
from flask import Flask, request, render_template, send_file
import cv2
from PIL import Image


app = Flask(__name__)


# # Load model.
# with open('fish_classifier.pkl', 'rb') as f:
#     model = pickle.load(f)


@app.route('/')
def home():
    """
    For rendering webpage.
    """
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    For rendering results on webpage.
    """

    image_file = request.files.get("image")

    # img = Image.open(image_file)
    # img = np.array(img)
    #
    # flipped_image = cv2.flip(img, 0)
    #
    # send_file(filename, mimetype='image/gif')

    send_file(image_file, mimetype="image/gif")
    # Render image
    # return render_template('index.html', prediction_text='Model returned no predictions.')
    

if __name__ == '__main__':
    app.run()
