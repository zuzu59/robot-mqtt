# python3.6
# Petit programme en python pour envoyer seulement la commande START sur le robot_0
# zf230122.1322
# Sources: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# Installation: pip3 install paho-mqtt
# Utilisation python3 send_start.py

import random
import time

from paho.mqtt import client as mqtt_client


broker = '192.168.20.107'
port = 1883
topic = "robot_0/switch/robot_0_motor_start/set"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'toto'
password = 'tutu'


def connect_mqtt():
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


def publish(client):
    time.sleep(2)
    result = client.publish(topic, "ON")
    status = result[0]
    if status == 0:
        print(f"Send ON to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    print("Hello zuzu")
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
