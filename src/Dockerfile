FROM python:3.11.4-bullseye
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN python -m pip install --upgrade pip

COPY requirements.txt /usr/src/app/
RUN python -m pip install --no-cache-dir -r requirements.txt

# Install dependencies
RUN apt update
RUN apt install -y ffmpeg libavcodec-extra alsa-utils

COPY . .