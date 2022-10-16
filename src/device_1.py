import certifi
import spidev, time
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import struct
import json
from light_sensor import MySPIDevice 
from cloud_config import SolaceMQTTConfig 

"""
Solace publisher
AWS IoT subscriber
"""

def main():
    ## Configuration    
    config_max_speed_hz = 1000000
    solace_topic = 'assignment_2'
    channel = 1
    path = 'solace_config.json'
    
    solaceSetting = SolaceMQTTConfig()
    solaceSetting.read_config_json(path)
    solaceSetting_dict = solaceSetting.to_dict()
    
    print(solaceSetting_dict)  
    
    device_1 = MySPIDevice()
    device_1.spi.max_speed_hz = config_max_speed_hz
    
    print("Setting...")
    
    ## Connect device to solace MQTT broker
    client = mqtt.Client('device_1')
    client.username_pw_set(username=solaceSetting_dict['username'], password=solaceSetting_dict['password'])
    client.tls_set(ca_certs=certifi.where())
    client.connect(solaceSetting_dict['url'],port=solaceSetting_dict['port'])
    
    
    print("Start Publishing")
    ## Publish Message
    while True:
        ## Get integer value of light
        light_value = device_1.analog_read(channel)
        payload_dict = {'light':light_value}
        payload = json.dumps(payload_dict)
        print(payload)
        
        ## Publish with Payload
        client.publish(solace_topic, payload=payload)
        
        time.sleep(1)
        

if __name__ == '__main__':
    main()