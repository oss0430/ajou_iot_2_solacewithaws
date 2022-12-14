import certifi
import time
import paho.mqtt.client as mqtt
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import json
import picamera
from cloud_config import SolaceMQTTConfig, AWSMQTTConfig
from bytes_encoder import picture_to_json
from AWS import aws_publish


"""
Solace subscriber
AWS IoT publisher

    Connect to Solace MQTT Broker,
    Asyncronously listen to Solace Messages using callback
    
    Everytime message is received connect to AWS IoT MQTT Broker,
    if requirement is met take picture and publish to AWS
"""

def main():
    ## Configuration
    ## Solace cloud configuration
    solace_topic = 'assignment_2'
    solace_path = './solace_config.json'
    client_id = 'device_2'

    aws_config_path = 'aws_config.json'
    solaceSetting = SolaceMQTTConfig()
    solaceSetting.read_config_json(solace_path)
    solaceSetting_dict = solaceSetting.to_dict()
    


    print(solaceSetting_dict)  
    
    awsSetting = AWSMQTTConfig()
    awsSetting.read_config_json(aws_config_path)
    awsSetting_dict = awsSetting.to_dict()
    print(awsSetting_dict)


    print("Setting...")
    solace_client = mqtt.Client(client_id)
    solace_client.username_pw_set(username=solaceSetting_dict['username'], password=solaceSetting_dict['password'])
    
    def on_connect(
        client,
        userdata,
        flags,
        rc
    ):  
        print("Connected with result code {0}".format(str(rc)))
        client.subscribe('assignment_2')

    ## Subscribe and Connect Solace
    def on_message(
        client,
        userdata,
        msg
    ):  
        print(msg.topic)

        ## AWS Cloud configuration
        aws_config_path = './aws_config.json'
        config_disconnection_timeout = 10
        config_mqtt_operation_timeout = 5
        client_id = 'device_2'
        aws_topic = "assignment_2"

        ## Load AWS cloud configuration
        awsSetting = AWSMQTTConfig()
        awsSetting.read_config_json(aws_config_path)
        awsSetting_dict = awsSetting.to_dict()

        ## Connect and Publish to AWS MQTT broker
        aws_client = AWSIoTPyMQTT.AWSIoTMQTTClient(client_id)
        aws_client.configureEndpoint(awsSetting_dict['host_name'], 8883) 
        aws_client.configureCredentials(awsSetting_dict['root_ca_path'], awsSetting_dict['private_key_path'], awsSetting_dict['cert_file_path']) 
        aws_client.configureConnectDisconnectTimeout(config_disconnection_timeout) 
        aws_client.configureMQTTOperationTimeout(config_mqtt_operation_timeout)
    
        def awsConnectCallback(mid, data):
            print("AWS connected")

        aws_client.connectAsync(ackCallback=awsConnectCallback)     

        json_data = json.loads(msg.payload)
        light_value = json_data['light']
        
        ## Check requirement
        threshold = 300
        if (light_value < threshold):
            
            ## Take Picture
            print("threshold crossed!")
            camera = picamera.PiCamera()
            camera.rotation = 90
            camera.resolution = (640,480)
            camera.start_preview()
            time.sleep(2) 
            camera.capture('picamera_liluminance.png')
            camera.close()
            
            ## Encode Picture
            filename = "picamera_liluminace.png"
            messageJson = picture_to_json(filename)
            
            ## Publish using AWS 
            def awsPublishcallback(mid):
                print("AWS Publish") 

            aws_client.publishAsync(aws_topic, messageJson, 1, ackCallback=awsPublishcallback)
    
    solace_client.on_connect = on_connect
    solace_client.on_message = on_message
    solace_client.tls_set(ca_certs=certifi.where())
    solace_client.connect(solaceSetting_dict['url'],solaceSetting_dict['port'])
    solace_client.loop_forever()

if __name__ == '__main__':
    main()
