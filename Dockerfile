FROM python:3

RUN apt-get update && apt-get install --no-install-recommends -y \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install opencv-python tensorflow cvlib

WORKDIR /usr/src/app

COPY main.py .
COPY sample.jpg .

RUN python main.py sample.jpg result --generate_image
