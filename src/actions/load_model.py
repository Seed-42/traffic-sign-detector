from config.app_config import APP_PRETRAINED_MODELS_PATH
from app_utils.gcloud_utils import download_models

import tensorflow as tf


def load_model():
    print("Model loading started.")
    model = tf.saved_model.load(APP_PRETRAINED_MODELS_PATH)
    print("Model loaded successfully.")
    return model


download_models()
MODEL = load_model()
