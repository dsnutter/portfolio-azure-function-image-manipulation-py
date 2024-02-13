import azure.functions as func
import logging
from PIL import Image
import json
from io import BytesIO
import base64
import math

CONTENT_TYPES_VALID = ('application/json', 'multipart/form-data')
IMAGE_TYPES_VALID = {'image/jpeg': 'JPEG', 'image/jpg': 'JPEG', 'image/png': 'PNG'}

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="v1/dimensions", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def dimensions(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing HTTP Triggered request for returning image dimensions.')

    # process image file sent in the request
    img = process_image(req)
    if type(img) == func.HttpResponse:
        return img

    if img:
        body = {'dimensions': {'width':img.width, 'height':img.height }}
        return func.HttpResponse(body=json.dumps(body, indent=4),
                                 headers={'Content-Type': 'application/json'},
                                 status_code=200)
    else:
        return return_error('Please pass a image in the body with mulitpart/form-data header, and a key of image for the image file.')

@app.route(route="v1/scale", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def scale(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing HTTP triggered request for resizing an image.')

    # process image file sent in the request
    img, type_request, type_image = process_image(req)
    if type(img) == func.HttpResponse:
        return img

    try:
        if type_request == CONTENT_TYPES_VALID[1]:
            temp = req.form
            item = temp.get('scale')
            scale = int(item)
        elif type_request == CONTENT_TYPES_VALID[0]:
            temp = req.get_json().get('scale')
            scale = int(temp)
        # scale down
        if scale < 0:
            img_scaled = img.resize((img.width // abs(scale) , img.height // abs(scale)))
        # scale up
        elif scale > 0:
            img_scaled = img.resize((img.width * scale, img.height * scale))
        # will not scale and just return the original image
        else:
            img_scaled = img
    except ValueError as e:
        logging.info(f"ValueError: Custom error catch: {e}")
        return return_error('Scale must be an integer.', status=400)
    except TypeError as e:
        logging.info(f"TypeError: Custom error catch: {e}")
        return return_error('Scale must be an integer.', status=400)
    except Exception as e:
        logging.info(f"Exception: Custom error catch: {e}")
        return return_error('Unknown error occurred.', status=500)

    if img:
        buffer = BytesIO()
        img_scaled.save(buffer, format=IMAGE_TYPES_VALID[type_image])
        # decode UTF8 removes b' from string
        base64image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        body = {
                'original_dimensions': {'width':img.width, 'height':img.height },
                'scaled_dimensions': {'width':img_scaled.width, 'height':img_scaled.height },
                'scale': scale,
                'img_scaled': f'data:{type_image};base64,{base64image}'
                }
        return func.HttpResponse(body=json.dumps(body, indent=4),
                                 headers={'Content-Type': 'application/json'},
                                 status_code=200)
    else:
        return return_error('Please pass a image file and a -/+ scale in the body with mulitpart/form-data header.')

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

    return return_error(msg, status)
