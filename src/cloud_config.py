import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

class SolaceMQTTConfig():

    def __init__(
        self,
        url = None,
        port = None,
        username = None,
        password = None,
        topic = None
    ):

        self.url = url
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic


    def read_config_json(
        self,
        path
    ):
        json_file = open(path)

        solace_data_dict = json.load(json_file)

        self.username = solace_data_dict['Username']
        self.password = solace_data_dict['Password']

        ## NOTE in python using url is different
        ## if url is 'ssl://myurl.messaging.solace.cloud:8883'
        ## client.connect(myurl.messaging.solace.cloud, port = 8883)

        full_url = solace_data_dict['Secured MQTT Host']

        url  = full_url[6:-5]
        port = int(full_url[-4:])

        self.url = url
        self.port = port



    def to_dict(
        self
    ):

        return {
            'url':self.url,
            'port':self.port,
            'username':self.username,
            'password':self.password
        }


class AWSMQTTConfig():

    def __init__(
        self,
        thing_name = None,
        host_name = None,
        root_ca_path = None,
        private_key_path = None,
        cert_file_path = None,
        disconnection_timeout = None,
        mqtt_operation_timeout = None
    ):

        self.thing_name = thing_name
        self.host_name = host_name
        self.root_ca_path = root_ca_path
        self.private_key_path = private_key_path
        self.cert_file_path = cert_file_path
        self.disconnection_timeout = disconnection_timeout
        self.mqtt_operation_timeout = mqtt_operation_timeout


    def read_config_json(
        self,
        path
    ):
        json_file = open(path)

        aws_data_dict = json.load(json_file)

        self.thing_name = aws_data_dict['Thing_Name']
        self.host_name = aws_data_dict['Host_Name']
        self.root_ca_path = aws_data_dict['Root_CA']
        self.private_key_path = aws_data_dict['Prviate_Key']
        self.cert_file_path = aws_data_dict['Cert_File']



    def to_dict(
        self
    ):

        return {
            'thing_name': self.thing_name,
            'host_name': self.host_name,
            'root_ca_path': self.root_ca_path,
            'private_key_path': self.private_key_path,
            'cert_file_path': self.cert_file_path,
            'disconnection_timeout': self.disconnection_timeout,
            'mqtt_operation_timeout': self.mqtt_operation_timeout
        }

    def create_client(
        self,
        client_id
    ):
        return AWSIoTPyMQTT.AWSIoTMQTTClient(client_id)