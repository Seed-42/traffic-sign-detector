from flask import Flask, request, jsonify, render_template, redirect, url_for, request, json
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from werkzeug.utils import secure_filename
from PIL import Image
import os
import tensorflow as tf
import base64
import cv2
import numpy as np
import io

from config import app_config
from actions.load_model import MODEL
from pathlib import Path

# location of label map
PATH_TO_LABELS = os.path.join(Path(__file__).parent, 'label_map.pbtxt')

# minimum required score for prediction
MIN_THRESH = 0.4

# max num of boxes/prediction to draw on the image
MAX_BOXES = 1

# load the label map
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

# initialize flask app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('HomePage.html')


@app.route('/predict', methods=['GET', 'POST'])
def process_image():
    label = []

    if request.method == 'POST':
        print("making prediction")

        #get the image and save it inside the upload folder located inside the static folder
        f = request.files['file']
        filename = secure_filename(f.filename)
        location = "static/img/upload/"+filename
        f.save(os.path.join('static/img/upload', filename))

        print("file saved at: " + location)

        #read the image using opencv
        image = cv2.imread(location)
        image =cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        #make predictions on the image
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # input_tensor = np.expand_dims(image_np, 0)
        detections = MODEL(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}

        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        for i in range(len(detections['detection_scores'])):
          if(detections['detection_scores'][i] >= MIN_THRESH):
              output = (category_index.get(detections['detection_classes'][i]).get('name'),detections['detection_scores'][i]*100)
              label.append(output)

        image_detections = image.copy()


        viz_utils.visualize_boxes_and_labels_on_image_array(
        image_detections,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates = True,
        max_boxes_to_draw = MAX_BOXES,
        min_score_thresh = MIN_THRESH,
        agnostic_mode = False)

        img = Image.fromarray(image_detections.astype("uint8"))
        rawBytes = io.BytesIO()
        img.save(rawBytes, "JPEG")
        encodedImg = base64.b64encode(rawBytes.getvalue())

        #sort based on 2nd element(score)
        label.sort(key = lambda x: x[1])
        data = {'location': str(encodedImg), 'predict': label}

        return jsonify(data), 200


if __name__ == '__main__':
    app.run(host=app_config.APP_HOST, port=app_config.APP_PORT)
