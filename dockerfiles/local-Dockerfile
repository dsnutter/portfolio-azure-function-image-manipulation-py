# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.11-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# BEGIN: Local docker use only - not for external use running in cloud
RUN mkdir /etc/secrets/
ENV FUNCTIONS_SECRETS_PATH=/etc/secrets
ENV AzureWebJobsSecretStorageType=Files
ADD local.host_secrets.json /etc/secrets/host.json
# END: Local docker use only - not for external use running in cloud

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot