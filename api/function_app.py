import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
def hello(req: func.HttpRequest) -> func.HttpResponse:
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

@app.route(route="video", auth_level=func.AuthLevel.ADMIN)
def video(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    blob = req.params.get('blob')
    if not blob:
        return func.HttpResponse("No blob specified.", status_code=401)

    url = f"https://d782.blob.core.windows.net/videos/{blob}"
    
    return func.HttpResponse(
        json.dumps({"url": url}), status_code=200,
        mimetype="application/json"
    )
    