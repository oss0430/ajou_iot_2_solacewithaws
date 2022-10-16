import json

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