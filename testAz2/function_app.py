import azure.functions as func
import logging
import csv

import csv
from datetime import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)




@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
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
        return func.HttpResponse(f"Hello, {name}. {csv.field_size_limit.__module__}This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             f"This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response. the value of a * b = ",
             status_code=200
        )

@app.route(route="http_trigger2")
def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
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
        return func.HttpResponse(f"2Hello, {name}. {csv.field_size_limit.__module__}This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             f"2This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response. the value of a * b = ",
             status_code=200
        )
    

    



@app.function_name(name="BlobOutput1")
@app.route(route="file")
@app.blob_input(arg_name="inputblob",
                path="zsblob/demokam.txt",
                connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob",
                path="zsblob/demokam.txt",
                connection="AzureWebJobsStorage")
def main(req: func.HttpRequest, inputblob: str, outputblob: func.Out[str]):
    logging.info(f'Python Queue trigger function processed {len(inputblob)} {inputblob} bytes')
    a = inputblob + str(datetime.now())
    outputblob.set(a)


    return "ok"