import json
import base64
import PIL.Image as Image
from pydoc_data.topics import topics


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)
    
    
def picture_to_bytes(
    filename
):
    data = {}
    with open(filename, mode='rb') as file:
        img = file.read()
        
    data['image'] = base64.b64encode(img)
    messageJson = json.dumps(data, cls=BytesEncoder)
    
    return messageJson


def message_to_picture(
    message,
    image_file_path
):
    """
        From message
        Extract Payload (json)
        Decode encoded image data
        Save image data to file to desired path
        Finally open the image file 
    """
    
    #json_data = json.load(message.payload)
    
    #encoded_image = json_data['image']
    
    encoded_image = message.payload
    decoded_image = base64.b64decode(encoded_image)

    with open(image_file_path, 'w+') as f:
        f.write(decoded_image)
    
    Image.open(image_file_path)
