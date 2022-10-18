import certifi
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import struct
import json
import picamera
from cloud_config import SolaceMQTTConfig, AWSMQTTConfig
from bytes_encoder import picture_to_bytes
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
    aws_config_path = 'aws_config.json'
    config_disconnection_timeout = 10
    config_mqtt_operation_timeout = 5
    client_id = 'device_2'
    solaceSetting = SolaceMQTTConfig()
    solaceSetting.read_config_json(path)
    solaceSetting_dict = solaceSetting.to_dict()
    
    print(solaceSetting_dict)  
    
    awsSetting = AWSMQTTConfig()
    awsSetting.read_config_json(aws_config_path)
    awsSetting_dict = awsSetting.to_dict()
    print(awsSetting_dict)


    print("Setting...")
    
    ## Connect device to solace MQTT broker
    client = mqtt.Client(client_id)
    client.username_pw_set(username=solaceSetting_dict['username'], password=solaceSetting_dict['password'])
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(ca_certs=certifi.where())

    client.connect(solaceSetting_dict['url'],solaceSetting_dict['port'])

    
    ## Connect and Publish to AWS MQTT broker
    Client = AWSIoTPyMQTT.AWSIoTMQTTClient(client_id)
    Client.configureEndpoint(awsSetting_dict['host_name'], 8883) 
    Client.configureCredentials(awsSetting_dict['root_ca_path'], awsSetting_dict['private_key_path'], awsSetting_dict['cert_file_path']) 
    Client.configureConnectDisconnectTimeout(config_disconnection_timeout) 
    Client.configureMQTTOperationTimeout(config_mqtt_operation_timeout)
    
    def awsConnectCallback(mid, data):
        print("AWS connected")
    
    Client.connectAsync(ackCallback=awsConnectCallback)

    def awsPublishcallback(mid):
        print("AWS Publish")
    

    aws_topic = "assignment_2"
    
    threshold = 1000
    if (light_value > threshold):
        
        print("threshold crossed!")
        camera = picamera.PiCamera()
        camera.rotation = 90
        camera.resolution = (640,480)
        camera.start_preview()
        time.sleep(2) 
        camera.capture('picamera_liluminance.png')
        
        
        filename = "picamera_liluminace.png"
        messageJson = picture_to_bytes(filename)
        Client.publishAsync(aws_topic, messageJson, 1, ackCallback=awsPublishcallback)
    
    client.loop_forever()

if __name__ == '__main__':
    main()
