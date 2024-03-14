FROM python:3.11.4-bullseye
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN python -m pip install --upgrade pip

# Install dependencies
RUN apt update
RUN apt install -y ffmpeg libavcodec-extra alsa-utils libpcsclite-dev swig gcc pcsc-tools

COPY requirements.txt /usr/src/app/
RUN python -m pip install --no-cache-dir -r requirements.txt


COPY . .