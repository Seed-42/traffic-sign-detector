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
ENV GS_CREDENTIALS '{"type": "service_account", "project_id": "seed42-traffic-sign-detector", "private_key_id": "3ddb8e47f91411d2af3a291f219c1483e6051a30", "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDkm0REf5IvJewJ\nO4GLY9vGKDlzFvsl4pFJFmeC+h1dX/frPz8AswdXQO9/SlCDOVgD3z9YARvkaDnO\nZrOOJ/RztDYMrJhmuGXXBnZRabSWxjZdz4R/QWSGcraOKjgG38yC1qnRiEKSuJnK\nMnD8infxqlQ4MO8WD+7wYL2J88GYMbn2osZxTexY4lNLTCaeUQinNtjwJY9h0e+N\nceRFqErgkeEFdX9HHD2QSNO27TPfcdhc+z0bhh4PUJGrTkpcoVrCbG2tGe/CYqHj\nVZXYhwOwg8e2dCh8AD8zKkB/727MrcidYm9UK3+wnn6klwtq9zwZjmfAK/QEZ9iS\np/vb4SpJAgMBAAECggEAA+4ZT2B0xdYUYuhYqGniGJVu5ZtL9ayZpCl/UOo/m7zq\nmesQQfDx+i/1H7AD5q05uQK38WMYflXEq6QxAUt1mYRSbkD/2dRtxMa/ltP3EH7N\n5uqdjwoAe+RVBNuCZp5z/IpX9X17rOkBSAkT6SJXLReJNquWfdkhhpULlFRVVbcg\nN1bhcA3uFbWpxez9avo1d+nd3okbtsaVny6aeEI9LRHuZ9/MApZPITLu1E0YSIzs\ndxaNcugYod/Kc09/1dRmuesEPgVx0MWbNsS/GcoGy6SaMQ4N4bB/083soULHMpH7\nYWZhrhR/Jqnz9yX2MuZN6YM2NI2y1kKmVXq2m7hFoQKBgQDz4StdLGoawIp3qn3+\nL4kjdPiMgFDi5D/V14x6W9oGCKHKTtGOzTQYT8rXah/6PpMN05B4ew776dpjR9Kn\n/tvzPvcRVF25PWk4+k+sADx9UtTPtLEK6UbAIYevxX9kI9NWr8DQO2hGhB5ioAAy\ni2QACYhsLSQRlsmcwBdtqXaF4QKBgQDv98f/v0PdrI38KCTweIuMHzv9lKDFlDUk\nBzM6w1Ge+Q2Xu1lOx9lt63tK0wCF3dTAEhzUcGYPfirtS9XaD99rXEbF7nrkGSqD\nwYk6sp4ze+jYMeBZn1bonbsqSPmTB7LNF4h8BHXZSpsVt9FW1wrbLF51AdOkyyHj\n7aNjjsphaQKBgGWxvyNbIeOF5jeAIImdyNHANORhnVj/VJ8XAr0DECbz8oMp2rhx\nWQfKPgsVdcAj164sSlHy/oyNN0Ou72ieHZmQ5/WR+IMF2Jqpxg8zCgY4RAVYk3q5\nS4dSdAIXmMdpKPc80moCW7kL3p/BmFN7THe3geuZ5zBucCOs9hgEUigBAoGAc8V1\nJfuewFm5fofXmnRtzsJa7PJBxlDEeodGvfjxbeL2HdfzNEDSs2dCakz2GZ92Ptv+\nMLexZZQXHbjSiYvS3Db+pgtyGo3RpxM+I6V9EZWcNoGJnXN0OHGwlKv0TG0QZEYQ\nQNTeDmEiBQ5T3rOMt0TmpUimVQDzbsV9aFDBbtECgYBy7LHhyKL6jeW9oUE/rly4\nfvpvN4x3DLMpSCwvsQ68wxfaC2KE4raXbYt+gziYxMOPHAZTyf6/2NM5gKncqko4\nvHbrdEaKo3gJfozo9Z5WFSQGH9Ec+aC4wty2KnfzF3Jdf+4KxFhB8/EVsJWxV+To\nMwZU4ROeSMPOGd7+N63+ZQ==\n-----END PRIVATE KEY-----\n", "client_email": "sa1-203@seed42-traffic-sign-detector.iam.gserviceaccount.com", "client_id": "108058205360137515633", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sa1-203%40seed42-traffic-sign-detector.iam.gserviceaccount.com"}'
ENV GS_MODELS_BUCKET_NAME seed42-traffic-sign-detector-models


# CMD exec gunicorn --bind :$APP_PORT --workers 1 --threads 8 --timeout 0 main:app
CMD exec gunicorn --bind 0.0.0.0:7000 --timeout=300 main:app