import certifi
import time
import paho.mqtt.client as mqtt
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import json
from light_sensor import MySPIDevice
from cloud_config import SolaceMQTTConfig, AWSMQTTConfig
from bytes_encoder import message_to_picture

"""
Solace publisher
AWS IoT subscriber
"""
    
    
def main():
    ## Configuration
    config_max_speed_hz = 1000000
    solace_topic = 'assignment_2'
    channel = 1
    solace_config_path = 'solace_config.json'

    config_disconnection_timeout = 10
    config_mqtt_operation_timeout = 5
    aws_config_path = 'aws_config.json'
    client_id = 'device_1'
    aws_topic = 'assignment_2'

    solaceSetting = SolaceMQTTConfig()
    solaceSetting.read_config_json(solace_config_path)
    solaceSetting_dict = solaceSetting.to_dict()
    print(solaceSetting_dict)

    awsSetting = AWSMQTTConfig()
    awsSetting.read_config_json(aws_config_path)
    awsSetting_dict = awsSetting.to_dict()
    print(awsSetting_dict)
    

    device_1 = MySPIDevice()
    device_1.spi.max_speed_hz = config_max_speed_hz

    print("Setting...")

    ## Connect device to solace MQTT broker
    solace_client = mqtt.Client(client_id)
    solace_client.username_pw_set(username=solaceSetting_dict['username'], password=solaceSetting_dict['password'])
    solace_client.tls_set(ca_certs=certifi.where())
    solace_client.connect(solaceSetting_dict['url'],port=solaceSetting_dict['port'])
    

    ## Connect and Subscribe to AWS MQTT broker
    aws_client = AWSIoTPyMQTT.AWSIoTMQTTClient(client_id)
    aws_client.configureEndpoint(awsSetting_dict['host_name'], 8883) 
    aws_client.configureCredentials(awsSetting_dict['root_ca_path'], awsSetting_dict['private_key_path'], awsSetting_dict['cert_file_path']) 
    aws_client.configureConnectDisconnectTimeout(config_disconnection_timeout) 
    aws_client.configureMQTTOperationTimeout(config_mqtt_operation_timeout)
    
    def awsConnectCallback(mid, data):
        print("AWS connected")
    
    aws_client.connectAsync(ackCallback=awsConnectCallback)

    def awsSubscribeCallback(mid, data):
        print("AWS Subscribed")
    
    
    def callbackonAWSMessage(client, userdata, message):
        print('message recieved')
        print(message.payload)
        #message_to_picture(message, 'received_picture.png')
    
    aws_client.subscribeAsync(aws_topic, 1, ackCallback = awsSubscribeCallback, messageCallback = callbackonAWSMessage)

    
    ## Publish Message with solace client
    print("Start Publishing")
    while True:
        ## Get integer value of light
        light_value = device_1.analog_read(channel)
        payload_dict = {'light':light_value}
        payload = json.dumps(payload_dict)
        print(payload)

        ## Publish with Payload
        solace_client.publish(solace_topic, payload=payload)

        time.sleep(1)


if __name__ == '__main__':
    main()
