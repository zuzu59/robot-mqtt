# python3.6

# ATTENTION n'est pas du tout terminé !

# Petit programme en python pour faire une petite démo avec le robot.
# Il avance au maximum contre un mur, recule un poil, tourne et repart au maximum.
# Ainsi il devrait tout balayer la zone
# zf230124.2129
# Sources: 
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# http://www.steves-internet-guide.com/into-mqtt-python-client/
# http://www.steves-internet-guide.com/send-json-data-mqtt-python/

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
robot_name = 'robot_2'
topic_distance = robot_name + "/sensor/" + robot_name + "_distance/state"
topic_start = robot_name + "/switch/" + robot_name + "_motor_start/set"
topic_stop = robot_name + "/switch/" + robot_name + "_motor_stop/set"
topic_forward = robot_name + "/switch/" + robot_name + "_motor_forward/set"
topic_backward = robot_name + "/switch/" + robot_name + "_motor_backward/set"
topic_left = robot_name + "/switch/" + robot_name + "_motor_left/set"
topic_right = robot_name + "/switch/" + robot_name + "_motor_right/set"




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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.payload.decode() != "nan" :
            if float(msg.payload.decode()) < 0.25 :
                print("Attention c'est plus petit que 25 cm")
            
    client.subscribe(topic_distance)
    client.on_message = on_message


def publish_commande(client, topic_commande):
    # envoie la commande ON au topic
    topic = topic_commande
    result = client.publish(topic, "ON")
    status = result[0]
    if status == 0:
        print(f"Send ON to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def publish_stop(client):
    # arrête le robot
    publish_commande(client,topic_stop)

def publish_avance_droit(client):
    # fait avancer le robot droit devant
    publish_commande(client,topic_forward)
    publish_commande(client,topic_start)
    
def go_demo(client):
    publish_avance_droit(client)
    time.sleep(3)
    publish_stop(client)
    


def run():
    print("Hello zuzu")
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    time.sleep(1)
    go_demo(client)


if __name__ == '__main__':
    run()
