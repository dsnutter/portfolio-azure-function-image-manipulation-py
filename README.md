Image Manipulation Azure Function using Python
==============================================
* API that manipulates images
    * Gettting image dimensions
    * Rescaling the image by a scale factor
    * Stripping out location data
* To connect to the API:
    * use scripts from powershell folder
    * use Postman
* To develop and run the azure funtions locally:
    * follow the instructions for VSCode below
    * "func start" to run from CLI using Azure CLI
* To run unit tests
    * cd azure_fn_image_manipulation
    * run "pytest"
    * or open "azure_fn_image_manipulation" in VSCode and run test that way

Requirements
============
* Python 3.11

Windows
=======
### For windows install
1. cd "azure_fn_image_manipulation"
2. py -m venv .venv
3. .\.venv\Scripts\activate
4. .\.venv\Scripts\python.exe -m pip install -r requirements.txt

### Additionally on windows for VSCode
1. ctrl-shift-p
2. Choose "Python: Create Environment"
3. Choose create venv
4. Use the existing python .venv from the .venv path created above
5. To run locally in vscode need Azurite Blob Service plugin running an instance of the test blob service

Local Docker Install Automatic
==============================
1. cd powershell/docker
2. ./standup.ps1 creates and runs the azure function docker container
3. ./teardown.ps1 stops and destroys the azure function docker container
4. After standing it up, you should be able to use the postman collections or powershell scripts to test

Local Docker Install Manual
===========================
1. cd azure_fn_image_manipulation
2. Create dockerfile: "func init --worker-runtime python --language python --docker --name fn_image_manipulation"
3. Use whatever tag you want an imamge name: "docker build --tag fn_image_manipulation:v1 ."
4. run container: "docker run -d -p 8080:80 fn_image_manipulation:v1"
5. see if running: "docker ps"
6. Go to "http://localhost:8080" and make sure get an azure function default response

![Azure Function Default Response](./docs/images/docker-default-azure-fn-get-response.png)

7. Access running container via: "docker exec -it container_id_from_ps /bin/bash"
8. To access logs use: "docker logs container_id_from_ps
9. Please use docker/external-cloud-Dockerfile for external deploymenets if using docker as docker/local-Dockerfile docker file sets a static x-functions-key
