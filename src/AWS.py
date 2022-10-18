import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import time



def aws_publish(
    self,
    topic,
    message_json,
    QoS
):
    Client_ID = "IoT_System_Client"
    Thing_Name = "pi_client"
    Host_Name = "a3d70y7w4oknm7-ats.iot.ap-northeast-2.amazonaws.com"
    Root_CA = "/home/pi/Desktop/DH_aws/AmazonRootCA1.crt"
    Private_Key = "/home/pi/Desktop/DH_aws/24e78fe6219276cddd0276cf3c78842d1a7ce1a64f152f9cf81f659d87eca7c5-private.pem.key"
    Cert_File = "/home/pi/Desktop/DH_aws/24e78fe6219276cddd0276cf3c78842d1a7ce1a64f152f9cf81f659d87eca7c5-certificate.pem.crt"

    Client = AWSIoTPyMQTT.AWSIoTMQTTClient(Client_ID)
    Client.configureEndpoint(Host_Name, 8883) 
    Client.configureCredentials(Root_CA, Private_Key, Cert_File) 
    Client.configureConnectDisconnectTimeout(10) 
    Client.configureMQTTOperationTimeout(5)
    Client.connect()
    
    Client.publish(topic, message_json, QoS)
    time.sleep(1)
    
