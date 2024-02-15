# azure-function-image-manipulation
* API that manipulates images using python and Azure. Test API calls are done with powershell
* To develop and run the azure funtions locally or run unit tests, open the "azure_fn_image_manipulation" folder in vscode

For windows
===========
1. cd "azure_fn_image_manipulation"
2. py -m venv .venv
3. .\.venv\Scripts\activate
4. .\.venv\Scripts\python.exe -m pip install -r requirements.txt

VSCode
======
1. ctrl-shift-p
2. Choose "Python: Create Environment"
3. Choose create venv
3. Use the existing python .venv from the .venv path created above

Docker
======
1. cd azure_fn_image_manipulation
2. Create dockerfile: "func init --worker-runtime python --language python --docker --name fn_image_manipulation"
3. Use whatever tag you want an imamge name: "docker build --tag fn_image_manipulation:v1 ."
4. run container: "docker run -d -p 8080:80 fn_image_manipulation:v1"
5. see if running: "docker ps"
6. Go to "http://localhost:8080" and make sure get an azure function default response
7. Access running container via: "docker exec -it container_id_from_ps /bin/bash"
8. To access logs use: "docker logs container_id_from_ps
9. Please use external-cloud-Dockerfile for external deploymenets if using docker as default docker file sets a static x-functions-key
