FROM python:3

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      ffmpeg \
      espeak-ng \
        libasound2 \
        alsa-utils \
        libsndfile1-dev && \
    apt-get clean

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY asound.conf /etc/asound.conf

CMD [ "python", "./mqtt2snapcast.py" ]