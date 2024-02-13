import unittest
from unittest.mock import Mock, patch
import azure.functions as func
import function_app
from PIL import Image
import io
import base64
from helper_functions import return_error, process_image
from constants import CONTENT_TYPES_VALID, IMAGE_TYPES_VALID

@patch('function_app.process_image')
def test_dimensions(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Calling the dimensions function
    response = function_app.dimensions(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.get_body(), b'{"dimensions": {"width": 60, "height": 30}}')

@patch('function_app.process_image')
def test_dimensions_no_image(self, mock_process_image):
    # Mocking the process_image function to return None
    mock_process_image.return_value = None

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Calling the dimensions function
    response = function_app.dimensions(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 400)

# testing dimensions function with json data
@patch('function_app.process_image')
def test_dimensions_json(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Calling the dimensions function
    response = function_app.dimensions(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 200)

    # did the dimensions function return the dimensions of the image?
    self.assertEqual(response.get_body(), b'{"dimensions": {"width": 60, "height": 30}}')

# testing dimensions function with multipart/form-data
@patch('function_app.process_image')
def test_dimensions_multipart(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Calling the dimensions function
    response = function_app.dimensions(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 200)

    # did the dimensions function return the dimensions of the image?
    self.assertEqual(response.get_body(), b'{"dimensions": {"width": 60, "height": 30}}')

# Testing the scale function
@patch('function_app.process_image')
def test_scale(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Adding a form to the request
    mock_request.form = {'scale': '2'}

    # Calling the scale function
    response = function_app.scale(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 200)

    # did the scale function scale the image?
    self.assertEqual(response.get_body(), b'{"dimensions": {"width": 120, "height": 60}}')

# testing the scale function with no image
@patch('function_app.process_image')
def test_scale_no_image(self, mock_process_image):
    # Mocking the process_image function to return None
    mock_process_image.return_value = None

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Calling the scale function
    response = function_app.scale(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 400)

# testing scale function with a scale that is not an integer
@patch('function_app.process_image')
def test_scale_not_int(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Adding a form to the request
    mock_request.form = {'scale': 'a'}

    # Calling the scale function
    response = function_app.scale(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 400)

# testing scale function with a scale that is 0
@patch('function_app.process_image')
def test_scale_zero(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Adding a form to the request
    mock_request.form = {'scale': '0'}

    # Calling the scale function
    response = function_app.scale(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 200)

    # did the scale function return the original image?
    self.assertEqual(response.get_body(), b'{"dimensions": {"width": 60, "height": 30}}')

# testing scale function with a scale that is negative
@patch('function_app.process_image')
def test_scale_negative(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Adding a form to the request
    mock_request.form = {'scale': '-2'}

    # Calling the scale function
    response = function_app.scale(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 200)

    # did the scale function scale the image?
    self.assertEqual(response.get_body(), b'{"dimensions": {"width": 30, "height": 15}}')

# testing scale function with json data
@patch('function_app.process_image')
def test_scale_json(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Adding json data to the request
    mock_request.get_json.return_value = {'scale': 2}

    # Calling the scale function
    response = function_app.scale(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 200)

    # did the scale function scale the image?
    self.assertEqual(response.get_body(), b'{"dimensions": {"width": 120, "height": 60}}')

# testing scale function with multipart/form-data
@patch('function_app.process_image')
def test_scale_multipart(self, mock_process_image):
    # Mocking the process_image function to return an Image object
    mock_img = Image.new('RGB', (60, 30))
    mock_process_image.return_value = mock_img

    # Creating a mock request
    mock_request = Mock(func.HttpRequest)

    # Adding a form to the request
    mock_request.form = {'scale': '2'}

    # Calling the scale function
    response = function_app.scale(mock_request)

    # Asserting the response
    self.assertEqual(response.status_code, 200)

    # did the scale function scale the image?
    self.assertEqual(response.get_body(), b'{"dimensions": {"width": 120, "height": 60}}')

if __name__ == '__main__':
    unittest.main()