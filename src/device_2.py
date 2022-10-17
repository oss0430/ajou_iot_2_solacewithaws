import certifi
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import struct
import json
from cloud_config import SolaceMQTTConfig 
from bytes_encoder import picture_to_byte
from AWS import aws_publish


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
    
    json_data = json.load(msg.payload)
    global light_value 
    light_value = json_data['light']


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
    

    aws_topic = "assignment_2"
    
    threshold = 1000
    if (light_value > threshold):
        '''
        camera = picamera.PiCamera()
        camera.rotation = 90
        camera.resolution = (640,480)
        camera.start_preview()
        time.sleep(2) 
        camera.capture('picamera_liluminance.jpg')
        '''
        
        filename = "picamera_practice.png"
        messageJson = picture_to_byte(filename)
        aws_publish(aws_topic, messageJson, 0)

        

if __name__ == '__main__':
    main()
