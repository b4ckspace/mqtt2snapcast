#!/usr/bin/env python
import time
import os
import subprocess
import sys

import paho.mqtt.client as mqtt

mqtt_host = os.environ.get('MQTT_BROKER', 'localhost')
mqtt_user = os.environ.get('MQTT_USER', None)
mqtt_pass = os.environ.get('MQTT_PASS', None)
mqtt_port = os.environ.get('MQTT_PORT', 1883)
snap_pipe = os.environ.get('SNAPCAST_FIFO', '/tmp/snapcast/soundboard')

if mqtt_user is not None:
    mqtt.username_pw_set(mqtt_user, mqtt_pass)

def play_tts(msg, lang="de"):
    pipe = "/tmp/snapcast/soundboard"
    bashCommand = "espeak-ng "
    bashCommand += "'"
    bashCommand += msg
    bashCommand += "' "
    bashCommand += "-v"
    bashCommand += lang
    bashCommand += " --stdout | ffmpeg -y -i pipe:0 -f u16le -acodec pcm_s16le -ac 2 -ar 48000 "
    bashCommand += snap_pipe
    print(bashCommand)
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True)

def on_connect(client, userdata, flags, rc):
    client.subscribe("psa/tts")
    client.subscribe("psa/tts/+")
    print("Connected to mqtt with result code " + str(rc))

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == "psa/tts":
        play_tts(payload)
    if topic != "psa/tts":
        play_tts(payload, topic.strip("psa/tts/"))
    print("RECEIVED: " + topic + '  ' + payload)

client = mqtt.Client()
client.on_connect = on_connect

client.connect(mqtt_host, mqtt_port, 60)
client.on_message = on_message
client.loop_start()

while True:
    time.sleep(2)
