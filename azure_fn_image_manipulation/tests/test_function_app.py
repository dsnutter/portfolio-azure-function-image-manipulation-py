import unittest
from unittest.mock import Mock, patch
import azure.functions as func
from PIL import Image
import io
import base64
from helper_functions import return_error, process_image
from constants import CONTENT_TYPES_VALID, IMAGE_TYPES_VALID
import function_app

class TestFunctionApp(unittest.TestCase):

    @patch('function_app.process_image')
    def test_dimensions_no_image(self, mock_process_image):
        # Mocking the process_image function to return None
        mock_process_image.return_value = None, None, None

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)

        # build the azure function dimensions to unit test it
        fn_call = function_app.dimensions.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 500

    # testing dimensions function with json data
    @patch('function_app.process_image')
    def test_dimensions_json(self, mock_process_image):
        # Mocking the process_image function to return an Image object
        mock_img = Image.new('RGB', (60, 30))
        mock_process_image.return_value = mock_img, 'application/json', 'image/jpeg'

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)

        # build the azure function dimensions to unit test it
        fn_call = function_app.dimensions.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 200

        assert str(response.get_body()).lower().find('"dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"width": 60') >= 0
        assert str(response.get_body()).lower().find('"height": 30') >= 0

    @patch('function_app.process_image')
    def test_dimensions_mulipart(self, mock_process_image):
        # Mocking the process_image function to return an Image object
        mock_img = Image.new('RGB', (60, 30))
        mock_process_image.return_value = mock_img, 'multipart/form-data', 'image/jpeg'

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)
        mock_request.headers = {'Content-Type': 'multipart/form-data'}

        # build the azure function dimensions to unit test it
        fn_call = function_app.dimensions.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 200
        assert str(response.get_body()).lower().find('"dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"width": 60') >= 0
        assert str(response.get_body()).lower().find('"height": 30') >= 0

    @patch('function_app.process_image')
    def test_scale_no_image(self, mock_process_image):
        # Mocking the process_image function to return None
        mock_process_image.return_value = None, 'application/json', 'image/jpeg'

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)
        mock_request.get_json.return_value = {'scale': 0}

        # build the azure function scale to unit test it
        fn_call = function_app.scale.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 500

    @patch('function_app.process_image')
    def test_scale_not_int(self, mock_process_image):
        # Mocking the process_image function to return an Image object
        mock_img = Image.new('RGB', (60, 30))
        mock_process_image.return_value = mock_img, 'application/json', 'image/jpeg'

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)

        # Adding a form to the request
        mock_request.form = {'scale': 'a'}

        # build the azure function scale to unit test it
        fn_call = function_app.scale.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 400

    @patch('function_app.process_image')
    def test_scale_zero(self, mock_process_image):
        # Mocking the process_image function to return an Image object
        mock_img = Image.new('RGB', (60, 30))
        mock_process_image.return_value = mock_img, 'application/json', 'image/jpeg'

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)
        mock_request.get_json.return_value = {'scale': 0}

        # build the azure function scale to unit test it
        fn_call = function_app.scale.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 200

        assert str(response.get_body()).lower().find('"scaled_dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"original_dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"width": 60') >= 0
        assert str(response.get_body()).lower().find('"height": 30') >= 0
        assert str(response.get_body()).lower().find('"scale": 0') >= 0

    @patch('function_app.process_image')
    def test_scale_negative(self, mock_process_image):
        # Mocking the process_image function to return an Image object
        mock_img = Image.new('RGB', (60, 30))
        mock_process_image.return_value = mock_img, 'application/json', 'image/jpeg'

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)
        mock_request.get_json.return_value = {'scale': -2}

        # build the azure function scale to unit test it
        fn_call = function_app.scale.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 200

        assert str(response.get_body()).lower().find('"scaled_dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"original_dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"width": 60') >= 0
        assert str(response.get_body()).lower().find('"height": 30') >= 0
        assert str(response.get_body()).lower().find('"width": 30') >= 0
        assert str(response.get_body()).lower().find('"height": 15') >= 0
        assert str(response.get_body()).lower().find('"scale": -2') >= 0

    @patch('function_app.process_image')
    def test_scale_json(self, mock_process_image):
        # Mocking the process_image function to return an Image object
        mock_img = Image.new('RGB', (60, 30))
        mock_process_image.return_value = mock_img, 'application/json', 'image/jpeg'

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)

        # Adding json data to the request
        mock_request.get_json.return_value = {'scale': 2}

        # build the azure function scale to unit test it
        fn_call = function_app.scale.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 200

        assert str(response.get_body()).lower().find('"scaled_dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"original_dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"width": 60') >= 0
        assert str(response.get_body()).lower().find('"height": 30') >= 0
        assert str(response.get_body()).lower().find('"width": 120') >= 0
        assert str(response.get_body()).lower().find('"height": 60') >= 0
        assert str(response.get_body()).lower().find('"scale": 2') >= 0

    @patch('function_app.process_image')
    def test_scale_multipart(self, mock_process_image):
        # Mocking the process_image function to return an Image object
        mock_img = Image.new('RGB', (60, 30))
        mock_process_image.return_value = mock_img, 'multipart/form-data', 'image/jpeg'

        # Creating a mock request
        mock_request = Mock(func.HttpRequest)

        # Adding a form to the request
        mock_request.form = {'scale': '2'}

        # build the azure function scale to unit test it
        fn_call = function_app.scale.build().get_user_function()        
        response = fn_call(mock_request)

        # Asserting the response
        assert response.status_code == 200

        assert str(response.get_body()).lower().find('"scaled_dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"original_dimensions":') >= 0 
        assert str(response.get_body()).lower().find('"width": 60') >= 0
        assert str(response.get_body()).lower().find('"height": 30') >= 0
        assert str(response.get_body()).lower().find('"width": 120') >= 0
        assert str(response.get_body()).lower().find('"height": 60') >= 0
        assert str(response.get_body()).lower().find('"scale": 2') >= 0

if __name__ == '__main__':
    unittest.main()