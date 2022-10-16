import spidev, time
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import struct
from light_sensor import MySPIDevice 
from cloud_config import SolaceMQTTConfig 

def main():
    
    ## Configuration    
    config_max_speed_hz = 1000000
    url = 
    username = 
    password = 
    channel = 1
    topic = 'Ajou_IoTSystem_Assignment2'
    
    solaceSetting = SolaceMQTTConfig(url, username, password)
    device_1 = MySPIDevice()
    device_1.spi.max_speed_hz = config_max_speed_hz
    
    print("Setting...")
    
    ## Connect device to solace MQTT broker
    client = mqtt.Client()
    #client.connect(solaceSetting.url)
    
    
    print("Start Publishing")
    ## Publish Message
    while True:
        ## Get integer value of light
        light_value = device_1.analog_read(channel)
        print(light_value)
        ## Pack it into struct
        #payload = struct.pack(">light", light_value)
        
        ## Publish with Payload
        #publish(topic,payload,qos=0,retain=false)
        
        time.sleep(1)
        

if __name__ == '__main__':
    main()