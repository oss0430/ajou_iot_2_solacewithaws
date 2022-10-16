import certifi
import spidev, time
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import struct
import json
from light_sensor import MySPIDevice 
from cloud_config import SolaceMQTTConfig 

def main():
    ## Configuration    
    config_max_speed_hz = 1000000
    
    ## NOTE in python using url is different
    ## if url is 'ssl://myurl.messaging.solace.cloud:8883'
    ## client.connect(myurl.messaging.solace.cloud, port = 8883)
    solace_url = 'myurl.messaging.solace.cloud'
    solace_port = 8883
    solace_username = ''
    solace_password = ''
    solace_topic = 'assignment_2'
    channel = 1
    
    
    #solaceSetting = SolaceMQTTConfig(url, username, password)
    device_1 = MySPIDevice()
    device_1.spi.max_speed_hz = config_max_speed_hz
    
    print("Setting...")
    
    ## Connect device to solace MQTT broker
    client = mqtt.Client('device_1')
    client.username_pw_set(username=solace_username, password=solace_password)
    client.tls_set(ca_certs=certifi.where())
    client.connect(solace_url,port=solace_port)
    
    
    print("Start Publishing")
    ## Publish Message
    while True:
        ## Get integer value of light
        light_value = device_1.analog_read(channel)
        payload_dict = {'light':light_value}
        payload = json.dumps(payload_dict)
        print(payload)
        
        ## Publish with Payload
        client.publish(solace_topic,payload,qos=0,retain=False)
        
        time.sleep(1)
        

if __name__ == '__main__':
    main()