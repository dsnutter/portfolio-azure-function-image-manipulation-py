import azure.functions as func
import logging
from PIL import Image
import json
from io import BytesIO
import base64
from helper_functions import return_error, process_image
from constants import CONTENT_TYPES_VALID, IMAGE_TYPES_VALID

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="v1/dimensions", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def dimensions(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing HTTP Triggered request for returning image dimensions.')

    # process image file sent in the request
    img, type_request, type_image  = process_image(req)
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
