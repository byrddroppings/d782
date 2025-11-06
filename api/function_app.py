import azure.functions as func
import datetime
import json
import logging
import os

from azure.storage.blob import (
    generate_blob_sas, BlobSasPermissions
)

app = func.FunctionApp()

@app.route(route="video-sas", auth_level=func.AuthLevel.ADMIN)
def videoSas(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    blob = req.params.get('blob')
    if not blob:
        return func.HttpResponse("No blob specified.", status_code=401)

    account = os.environ["STORAGE_ACCOUNT_NAME"]
    key = os.environ["STORAGE_ACCOUNT_KEY"]
    container = os.environ.get("VIDEO_CONTAINER", "videos")
    now = datetime.datetime.utcnow()

    sas = generate_blob_sas(
        account_name=account,
        container_name=container,
        blob_name=blob,
        account_key=key,
        permission=BlobSasPermissions(read=True),
        expiry=now + datetime.timedelta(minutes=5),
        start=now - datetime.timedelta(minutes=1),  # clock skew
        ip=None,  # optionally lock to an IP/CIDR
        protocol="https"
    )

    url = f"https://{account}.blob.core.windows.net/{container}/{blob}?{sas}"
    
    return func.HttpResponse(
        json.dumps({"url": url}), status_code=200,
        mimetype="application/json"
    )
    

@app.route(route="video", auth_level=func.AuthLevel.ADMIN)
def video(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    blob = req.params.get('blob')
    if not blob:
        return func.HttpResponse("No blob specified.", status_code=401)

    account = os.environ["STORAGE_ACCOUNT_NAME"]
    container = os.environ.get("VIDEO_CONTAINER", "videos")

    url = f"https://{account}.blob.core.windows.net/{container}/{blob}"
    
    return func.HttpResponse(
        json.dumps({"url": url}), status_code=200,
        mimetype="application/json"
    )
