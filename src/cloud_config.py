import json


class SolaceMQTTConfig():
    
    def __init__(
        self,
        url=none,
        username=none,
        password=none,
        topic=none
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
        
        with = open(path) as json_file:
            solace_data_dict = json_load(json_file)
            
            self.username = solace_data_dict['Username']
            self.password = solace_data_dict['Password']
            
            full_url = solace_data_dict['Secured MQTT Host']
            
        
        
        
        