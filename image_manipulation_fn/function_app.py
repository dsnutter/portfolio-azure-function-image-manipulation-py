import azure.functions as func
import logging
from PIL import Image
import json
from io import BytesIO
import base64

CONTENT_TYPES_VALID = ('application/json', 'multipart/form-data')

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
    img = process_image(req)

    try:
        scale = int(req.body.get('scale'))
        img_scaled = img.resize((img.width * scale, img.height * scale))
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
        body = {
                'original_dimensions': {'width':img.width, 'height':img.height },
                'scaled_dimensions': {'width':img_scaled.width, 'height':img_scaled.height },
                'scale': scale,
                'img_scaled': 'data:image/jpeg;base64,' + img_scaled.tobytes().decode('utf-8')
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
    try:
        header = req.headers['Content-Type']
        logging.info(f"Content-Type: {header}")
        valid_header = [header is not None and header.find(content_type) >= 0 for content_type in CONTENT_TYPES_VALID]
        if True not in valid_header:
            return return_error(f'Content-Type must be {content_type}', status=400)

        # multipart/form-data, binary image
        if header.find(CONTENT_TYPES_VALID[1]) >= 0:
            image_data = req.files['image']
        # application/json, base64 image
        elif header.find(CONTENT_TYPES_VALID[0]) >= 0:
            image_types = ['image/jpeg', 'image/jpg', 'image/png']
            image_data = req.get_json().get('image')
            for image_type in image_types:
                if image_data.find(image_type) >= 0:
                    image_data = image_data.replace(f'data:{image_type};base64,', '')

            # convert image_data to readable by PIL
            image_data = BytesIO(base64.b64decode(image_data))
        else:
            raise ValueError("Header image format was not correct")

        img = Image.open(image_data)
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
        return img

    return return_error(msg, status)
