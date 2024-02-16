import azure.functions as func
import logging
from PIL import Image
import json
from io import BytesIO
import base64
from constants import CONTENT_TYPES_VALID, IMAGE_TYPES_VALID

def return_error(msg, status=500):
    body = {'error': f'{msg}'}
    return func.HttpResponse(
        body=json.dumps(body, indent=4),
        headers={'Content-Type': 'application/json'},
        status_code=status)

def process_image(req, content_type='application/json'):
    type_request = None
    type_image = None
    try:
        header = req.headers['Content-Type']
        logging.info(f"Content-Type: {header}")
        valid_header = [header is not None and header.find(content_type) >= 0 for content_type in CONTENT_TYPES_VALID]
        if True not in valid_header:
            return return_error(f'Content-Type must be {content_type}', status=400)

        # multipart/form-data, binary image
        if header.find(CONTENT_TYPES_VALID[1]) >= 0:
            image_data = req.files['image']
            type_request = CONTENT_TYPES_VALID[1]
        # application/json, base64 image
        elif header.find(CONTENT_TYPES_VALID[0]) >= 0:
            image_data = req.get_json().get('image')
            for temp_type in IMAGE_TYPES_VALID.keys():
                if image_data.find(temp_type) >= 0:
                    image_data = image_data.replace(f'data:{temp_type};base64,', '')
                    break

            # convert image_data to readable by PIL
            image_data = BytesIO(base64.b64decode(image_data))
            type_request = CONTENT_TYPES_VALID[0]
        else:
            raise ValueError("Header image format was not correct")

        img = Image.open(image_data)

        # figure out what type of image it is that was passed in, JPGE, PNG, etc. and track it
        type_images = next(filter(lambda x: img.format == x[1], IMAGE_TYPES_VALID.items()))
        type_image = type_images[0]

    except ValueError as e:
        logging.info(f"ValueError: Custom error catch: {e}")
        msg = 'Error with value occurred.'
        status = 400
    except TypeError as e:
        logging.info(f"TypeError: Custom error catch: {e}")
        msg = 'Error with typing occurred.'
        status = 400
    except Exception as e:
        logging.info(f"Exception: Custom error catch: {e}")
        msg = 'Unknown error occurred.'
        status = 500
    else:
        return img, type_request, type_image

    return return_error(msg, status), type_request, type_image
