# python3.6

# ATTENTION n'est pas du tout terminé !

# Petit programme en python pour faire une petite démo avec le robot.
# Il avance au maximum contre un mur, recule un poil, tourne et repart au maximum.
# Ainsi il devrait tout balayer la zone
# zf230124.2329
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
topic_forward = robot_name + "/switch/" + robot_name + "_motor_direction_forward/set"
topic_backward = robot_name + "/switch/" + robot_name + "_motor_direction_backward/set"
topic_left = robot_name + "/switch/" + robot_name + "_motor_direction_left/set"
topic_right = robot_name + "/switch/" + robot_name + "_motor_direction_right/set"
topic_motor_time = robot_name + "/number/" + robot_name + "_motor_time/set"
topic_preburn = robot_name + "/number/" + robot_name + "_motor_preburn/set"
topic_preburn_time = robot_name + "/number/" + robot_name + "_motor_preburn_time/set"
robot_stoped = 0



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
                # client.loop_stop()
                publish_recule_tourne_left(client)
            
    client.subscribe(topic_distance)
    client.on_message = on_message

# envoie la commande ON au topic
def publish_command(client, topic_command):
    result = client.publish(topic_command, "ON")
    status = result[0]
    if status == 0:
        print(f"Send ON to topic `{topic_command}`")
    else:
        print(f"Failed to send message to topic {topic_command}")
    time.sleep(0.5)

# envoie une valeur au topic
def publish_consign(client, topic_number, topic_value):
    MQTT_MSG = '{"value":' + str(topic_value) + '}'
    result = client.publish(topic_number, MQTT_MSG)
    status = result[0]
    if status == 0:
        print(f"Send `{topic_value}` to topic `{topic_number}`")
    else:
        print(f"Failed to send message to topic {topic_number}")
    time.sleep(0.5)

# arrête le robot
def publish_stop(client):
    publish_command(client,topic_stop)

# fait avancer le robot droit devant
def publish_avance_droit(client):
    publish_command(client,topic_forward)
    publish_command(client,topic_start)

# recule 1 seconde puis tourne 1 seconde
def publish_recule_tourne_left(client):
    global robot_stoped
    print("robot_stoped: " + str(robot_stoped))
    if robot_stoped == 0 :
        robot_stoped = 1
        print("robot_stoped: " + str(robot_stoped))
        publish_consign(client, topic_preburn, 100)
        publish_consign(client, topic_preburn_time, 1)
        time.sleep(1)
        publish_command(client,topic_backward)
        publish_consign(client, topic_motor_time, 2)
        publish_command(client,topic_go)
        time.sleep(4)
        publish_command(client,topic_left)
        publish_consign(client, topic_motor_time, 2)
        publish_command(client,topic_go)
        time.sleep(4)
        # robot_stoped = 0
        # publish_avance_droit(client)



    
def go_demo(client):
    # publish_recule_tourne_left(client)
    publish_avance_droit(client)
    time.sleep(23)
    # # publish_stop(client)



def run():
    print("Hello zuzu")
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    time.sleep(1)
#    publish_consign(client, topic_motor_time, 1.25)
    go_demo(client)
    

if __name__ == '__main__':
    run()
