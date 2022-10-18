import json
import base64
from pydoc_data.topics import topics

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)
    
    
def picture_to_bytes(
    self,
    filename
):
    data = {}
    with open(filename, mode='rb') as file:
        img = file.read()
        
    data['image'] = base64.b64encode(img)
    messageJson = json.dumps(data, cls=BytesEncoder)
    
    return messageJson