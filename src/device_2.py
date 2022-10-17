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
    
def on_connect(
    client,
    userdata,
    flags,
    rc
):  
    print("Connected with result code {0}".format(str(rc)))
    
    
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
    
    #client.tls_set(ca_certs=certifi.where())
    
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
            client.connect(solaceSetting_dict['url'],port=1883)
            print(connected)
            
        except:
            print('failed to subscribe')
        #client.subscribe(solace_topic,0)
        time.sleep(1)
        

if __name__ == '__main__':
    main()