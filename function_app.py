import azure.functions as func
import logging
from PIL import Image
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="v1/dimensions", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def dimensions(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing HTTP Triggered request for image dimensions.')

    try:
        header = req.headers['Content-Type']
        logging.info(f"Content-Type: {header}")
        if header is None or header.find('multipart/form-data') == -1:
            return func.HttpResponse("{'error': 'Content-Type must be multipart/form-data'}", status_code=400)

        image_data = req.files['image']
        # image_data = req_body.get('image')
        img = Image.open(image_data)
    except ValueError as e:
        logging.info(f"ValueError: Custom error catch: {e}")
    except TypeError as e:
        logging.info(f"TypeError: Custom error catch: {e}")
    except Exception as e:
        logging.info(f"Exception: Custom error catch: {e}")

    if image_data:
        body = {'dimensions': {'width':img.width, 'height':img.height }}
        return func.HttpResponse(body=json.dumps(body, indent=4),
                                 headers={'Content-Type': 'application/json'},
                                 status_code=200)
    else:
        body = {'error': 'Please pass a image in the body with mulitpart/form-data header, and a key of image for the image file.'}
        return func.HttpResponse(
            body=json.dumps(body, indent=4),
            headers={'Content-Type': 'application/json'},
            status_code=200)

@app.route(route="v1/proportionize", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def proportionize(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )