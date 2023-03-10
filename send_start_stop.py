# python3.6
# Petit programme en python pour envoyer seulement la commande START 
# puis après quelques secondes la commande STOP sur le robot
# zf230122.1412
# Sources: 
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# http://www.steves-internet-guide.com/into-mqtt-python-client/
# Installation: pip3 install paho-mqtt
# Utilisation python3 send_start.py

import random
import time

from paho.mqtt import client as mqtt_client


broker = '192.168.20.107'
port = 1883
#topic = "robot_0/switch/robot_0_motor_start/set"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'toto'
password = 'tutu'
robot_name = 'robot_0'



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
    topic = robot_name + "/switch/" + robot_name + "_motor_start/set"
    time.sleep(1)
    result = client.publish(topic, "ON")
    status = result[0]
    if status == 0:
        print(f"Send ON to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    topic = robot_name + "/switch/" + robot_name + "_motor_stop/set"
    time.sleep(3)
    result = client.publish(topic, "ON")
    status = result[0]
    if status == 0:
        print(f"Send ON to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    print("Hello zuzu")
    client = connect_mqtt()
    publish(client)


if __name__ == '__main__':
    run()
