FROM python:3

RUN pip install opencv-python tensorflow cvlib

WORKDIR /usr/src/app

COPY main.py .
