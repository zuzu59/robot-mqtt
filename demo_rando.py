# python3.6

# ATTENTION n'est pas du tout terminé !

# Petit programme en python pour faire une petite démo avec le robot.
# Il avance au maximum contre un mur, recule un poil, tourne et repart au maximum.
# Ainsi il devrait tout balayer la zone
# zf230124.2211
# Sources: 
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# http://www.steves-internet-guide.com/into-mqtt-python-client/
# http://www.steves-internet-guide.com/send-json-data-mqtt-python/

# Installation: pip3 install paho-mqtt
# Utilisation python3 send_start.py

import random
import time
import json


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
topic_go = robot_name + "/switch/" + robot_name + "_motor_go/set"
topic_forward = robot_name + "/switch/" + robot_name + "_motor_forward/set"
topic_backward = robot_name + "/switch/" + robot_name + "_motor_backward/set"
topic_left = robot_name + "/switch/" + robot_name + "_motor_left/set"
topic_right = robot_name + "/switch/" + robot_name + "_motor_right/set"
topic_motor_time = robot_name + "/number/" + robot_name + "_motor_time/set"




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





def publish_command(client, topic_command):
    # envoie la commande ON au topic
    result = client.publish(topic_command, "ON")
    status = result[0]
    if status == 0:
        print(f"Send ON to topic `{topic_command}`")
    else:
        print(f"Failed to send message to topic {topic_command}")







def publish_consign(client, topic_number, topic_value):
    # envoie une valeur au topic
    MQTT_MSG = '{"value":' + str(topic_value) + '}'
    result = client.publish(topic_number, MQTT_MSG)
    status = result[0]
    if status == 0:
        print(f"Send `{topic_value}` to topic `{topic_number}`")
    else:
        print(f"Failed to send message to topic {topic_number}")

def publish_stop(client):
    # arrête le robot
    publish_command(client,topic_stop)

def publish_avance_droit(client):
    # fait avancer le robot droit devant
    publish_command(client,topic_forward)
    publish_command(client,topic_start)

def publish_recule_tourne_left(client):
    # recule 1 seconde puis tourne 1 seconde
    publish_command(client,topic_backward)
    # publish_consign(client, topic_motor_time, 1)
    # publish_command(client,topic_go)
    # time.sleep(1)
    # publish_command(client,topic_left)
    # publish_consign(client, topic_motor_time, 1)
    # publish_command(client,topic_go)
    # time.sleep(1)







    
def go_demo(client):
    # publish_avance_droit(client)
    # time.sleep(3)
    # publish_stop(client)
#    publish_recule_tourne_left(client)
    publish_command(client,topic_backward)



def run():
    print("Hello zuzu")
    client = connect_mqtt()
    # subscribe(client)
    # client.loop_start()
    time.sleep(2)
#    publish_consign(client, topic_motor_time, 1.25)
#    go_demo(client)
    publish_command(client,topic_backward)


if __name__ == '__main__':
    run()
