# python3.6
# Petit programme en python pour lire la distance du capteur de distance du robot
# zf230120.1813
# Sources: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# Installation: pip3 install paho-mqtt
# Utilisation python3 toto.py

import random

from paho.mqtt import client as mqtt_client

broker = '192.168.20.107'
port = 1883
topic = "robot_0/sensor/robot_0_distance/state"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'toto'
password = 'tutu'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
