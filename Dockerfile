#FROM python:3.6.9-slim-stretch
FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"

# Basic python packages.
RUN apt-get update && apt-get install -y pkg-config \
                                        build-essential \
                                        python3-pip \
                                        python3-dev \
                                        python3-distutils \
                                        python3-pkg-resources \
                                        python3-tk \
                                        git \
                                        libquadmath0 \
                                        ffmpeg \
                                        libsm6 \
                                        libxext6
#                                         python3-opencv \
#                                         libgl1-mesa-glx \
# End of basic python packages.


#### Object Detection modules

# clone the repository
RUN git clone --depth 1 https://github.com/tensorflow/models.git
# Install object detection api dependencies
RUN apt-get install -y protobuf-compiler python3-pil python3-lxml
# Get protoc 3.0.0, rather than the old version already in the container
# RUN curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" && \
#     unzip protoc-3.0.0-linux-x86_64.zip -d proto3 && \
#     mv proto3/bin/* /usr/local/bin && \
#     mv proto3/include/* /usr/local/include && \
#     rm -rf proto3 protoc-3.0.0-linux-x86_64.zip
# Run protoc on the object detection repo
RUN cd models/research && protoc object_detection/protos/*.proto --python_out=.
# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH=$PYTHONPATH:/models/research/object_detection
ENV PYTHONPATH=$PYTHONPATH:/models/research/slim
ENV PYTHONPATH=$PYTHONPATH:/models/research

WORKDIR /
#### End of object detection modules

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN mkdir -p /app/logs && touch /app/logs/app.log
WORKDIR /app
RUN mkdir -p /app/tmp
RUN mkdir -p /app/models
COPY src/ .

ENV APP_HOST 0.0.0.0
ENV APP_PORT 7000
ENV APP_LOG_PATH /app/logs
ENV APP_LOG_LEVEL DEBUG
ENV APP_TEMP_PATH /app/tmp
ENV APP_PRETRAINED_MODELS_PATH /app/models
ENV GS_MODELS_BUCKET_NAME seed42-traffic-sign-detector-models


# CMD exec gunicorn --bind :$APP_PORT --workers 1 --threads 8 --timeout 0 main:app
CMD exec gunicorn --bind 0.0.0.0:7000 --timeout=300 main:app