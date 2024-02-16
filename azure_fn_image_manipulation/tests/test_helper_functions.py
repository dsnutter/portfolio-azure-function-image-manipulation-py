import unittest
from unittest.mock import Mock, patch
import azure.functions as func
import function_app
from PIL import Image
import base64
from helper_functions import return_error, process_image
from io import BytesIO
from tests.constants_for_testing import BASE64_IMAGE, BASE64_IMAGE_HEIGHT, BASE64_IMAGE_WIDTH

# for testing mulitpart images with file support
from werkzeug.datastructures import FileStorage

# testing return_error function
def test_return_error():
    msg = 'This is an error message.'
    response = return_error(msg, status=400)
    assert response.status_code == 400
    assert str(response.get_body()).lower().find('"error":') >= 0
    assert str(response.get_body()).lower().find(msg.lower()) >= 0

# testing process_image function with json data
def test_process_image_json():

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)
    mock_request.get_json.return_value = {'image': 'data:image/jpeg;base64,' + BASE64_IMAGE}
    mock_request.headers = {'Content-Type': 'application/json'}

    # Calling the process_image function
    img, type_request, type_image = process_image(mock_request)

    # Asserting the response
    assert type_request == 'application/json'
    assert type_image == 'image/jpeg'
    assert img.width == BASE64_IMAGE_WIDTH
    assert img.height == BASE64_IMAGE_HEIGHT


# testing process_image function with multipart/form-data
def test_process_image_multipart():

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    image_data = base64.b64decode(bytes(BASE64_IMAGE.encode('UTF-8')))
    image_file = FileStorage(
        stream=BytesIO(image_data),
        filename="2.jpg",
        content_type="image/jpeg"
    )
    mock_request.files = {'image': image_file}

    #base64.b64encode(input=io.BytesIO(BASE64_IMAGE), output=temp)
    # mock_request.files = {'image': image_data}
    mock_request.headers = {'Content-Type': 'multipart/form-data'}

    # Calling the process_image function
    img, type_request, type_image = process_image(mock_request)

    # Asserting the response
    assert type_request == 'multipart/form-data'
    assert type_image == 'image/jpeg'
    assert img.width == BASE64_IMAGE_WIDTH
    assert img.height == BASE64_IMAGE_HEIGHT

# if __name__ == '__main__':
#     unittest.main()