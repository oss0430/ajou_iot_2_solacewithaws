import certifi
import spidev, time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import RPi.GPIO as gpio
import struct
import json
from cloud_config import SolaceMQTTConfig 

"""
Solace subscriber
AWS IoT publisher
"""


## Callback on_subscribe
"""    
def on_subscribe(
    client,
    obj,
    mid,
    granted_qos
):  
    print("Subscirbed: " + str(mid) + " " + str(granted_qos))
    
def on_log(
    client,
    obj,
    level,
    string
):  
    print(string)
"""
def print_msg(client, userdata, message):
    print(message)
    print(message.payload)

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
    #client = mqtt.Client('device_2')
    #client.username_pw_set(username=solaceSetting_dict['username'], password=solaceSetting_dict['password'])
    #client.tls_set(ca_certs=certifi.where())
    #client.connect(solaceSetting_dict['url'],port=solaceSetting_dict['port'])
    
    #client.on_subscribe = on_subscribe
    #client.on_log = on_log
    
    #print("Connected, start subscribing")
    ##client.subscribe(solace_topic)
    ## Publish Message
    while True:
        ## Get Msg
        
        #msg = subscribe.simple([solace_topic], hostname=solaceSetting_dict['url'], retained=False, msg_count = 2)
        #print(msg.payload)
        
        try : 
            msg = subscribe.simple(solace_topic, hostname = solaceSetting_dict['url'], retained=False)
          
            print(msg.topic)
            print(msg.payload)
        
        except:
            print('failed to subscribe')
        #client.subscribe(solace_topic,0)
        time.sleep(1)
        

if __name__ == '__main__':
    main()