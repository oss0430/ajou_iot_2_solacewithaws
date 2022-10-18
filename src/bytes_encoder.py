import cv2
import numpy as np
import json
import base64
from pydoc_data.topics import topics


    
def picture_to_json(
    file_path
):  
    """
        From image
        Convert to bytes
        Convert to json
    """

    img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    nothing, img_jpg = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    b64 = base64.b64encode(img_jpg)
    messageJson = json.dumps({'image':b64.decode("utf-8")})
    
    return messageJson


def json_to_picture(
    messageJson,
    image_file_path
):
    """
        From message
        Extract Payload (json)
        Decode encoded image data
        Save image data to file to desired path
        Finally open the image file 
    """
    
    b64 = json.loads(messageJson)

    img_jpg = base64.b64decode(b64['image'])
    img_na = cv2.imdecode(np.frombuffer(img_jpg,dtype=np.uint8), cv2.IMREAD_COLOR)
    cv2.imwrite(image_file_path, img_na) 

"""
def test_image_encode_decode(
    original_path,
    export_path
):
    messageJson = picture_to_json(original_path)
    print(len(messageJson))
    json_to_picture(messageJson,export_path)

    
test_image_encode_decode(
    'picamera_liluminance.png',
    'new.png'
)
"""