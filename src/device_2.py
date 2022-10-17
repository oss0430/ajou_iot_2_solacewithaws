import certifi
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import struct
import json
from cloud_config import SolaceMQTTConfig 

"""
Solace subscriber
AWS IoT publisher
"""


## Callback on_subscribe
    
def on_connect(
    client,
    userdata,
    flags,
    rc
):  
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe('assignment_2')

    
def on_message(
    client,
    userdata,
    msg
):  
    print(msg.topic)
    print(msg.payload)


def main():
    ## Configuration    
    solace_topic = 'assignment_2'
    channel = 1
    path = 'solace_config.json'
    
    solaceSetting = SolaceMQTTConfig()
    solaceSetting.read_config_json(path)
    solaceSetting_dict = solaceSetting.to_dict()
    
    print(solaceSetting_dict)  
    
    print("Setting...")
    
    ## Connect device to solace MQTT broker
    client = mqtt.Client('device_2')
    client.username_pw_set(username=solaceSetting_dict['username'], password=solaceSetting_dict['password'])
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(ca_certs=certifi.where())

    client.connect(solaceSetting_dict['url'],solaceSetting_dict['port'])

    client.loop_forever()

        

if __name__ == '__main__':
    main()
