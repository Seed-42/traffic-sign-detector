import os
import shutil

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# App credentials.
APP_HOST = os.environ.get("APP_HOST")
APP_PORT = os.environ.get("APP_PORT")
if APP_PORT:
    APP_PORT = int(APP_PORT)

# Logs.
APP_LOG_PATH = os.environ.get("APP_LOG_PATH")
APP_LOG_LEVEL = os.environ.get("APP_LOG_LEVEL", "DEBUG")
APP_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ML
APP_PRETRAINED_MODELS_PATH = os.environ.get("APP_PRETRAINED_MODELS_PATH")

# # GCLOUD
GS_CREDENTIALS = os.environ.get("GS_CREDENTIALS", "")
GS_MODELS_BUCKET_NAME = os.environ.get("GS_MODELS_BUCKET_NAME", "")
if not all([GS_CREDENTIALS, GS_MODELS_BUCKET_NAME]):
    raise Exception("Google Storage credentials missing.")

# TEMP
APP_TEMP_PATH = os.environ.get("APP_TEMP_PATH")

# Create paths if not exist.
for path in [APP_TEMP_PATH, APP_LOG_PATH, APP_PRETRAINED_MODELS_PATH]:
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
