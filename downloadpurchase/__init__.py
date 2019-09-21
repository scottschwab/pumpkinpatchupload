import logging

import azure.functions as func
import json
import csv
import uuid
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(req: func.HttpRequest, pumpkinstore: func.DocumentList) -> func.HttpResponse:
    logger.info('Python HTTP trigger function processed a request.')

# SELECT * FROM c WHERE c.type='pumpkin order' ORDER BY c._ts
#
    fieldnames = ['id','_ts', 'type', 'grand_total', 'donation']
    buffer = io.BytesIO()
    writer = csv.DictWriter(buffer, fieldnames)
    for order in pumpkinstore.get():
        if order["type"] == "pumpkin order":
            logger.info(order)
            writer.writerow(order)

    return func.HttpResponse(status_code=200)
