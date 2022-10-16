import spidev, time
import paho.mqtt.clinet as mqtt
import RPi.GPIO as gpio
import struct

import light_sensor
import cloud_config

def main():
    
    ## Configuration    
    max_speed_hz = 1000000
    url = ''
    username = ''
    password = ''
    channel = 1
    topic = 'Ajou_IoTSystem_Assignment2'
    
    solaceSetting = SolaceMQTTConfig(url, username, password)
    device_1 = MySPIDevice(max_speed_hz)
    
    
    ## Connect device to solace MQTT broker
    client = mqtt.Client()
    client.connect(solaceSetting.url)
    
    
    ## Publish Message
    while True:
        ## Get integer value of light
        light_value = device_1.analog_read(channel)
        
        ## Pack it into struct
        payload = struct.pack("light", light_value)
        
        ## Publish with Payload
        publish(topic,payload,qos=0,retain=false)
        
        sleep(1)