import logging

import azure.functions as func
import json
import csv
import uuid
import io



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(req: func.HttpRequest, pumpkinstore: func.DocumentList, outputblob: func.Out[func.InputStream]) -> func.HttpResponse:
    logger.info('Python HTTP trigger function processed a request.')

# SELECT * FROM c WHERE c.type='pumpkin order' ORDER BY c._ts
#
    fieldnames = ['id','_ts', 'type', 'grand_total', 'donation']
    buffer = io.StringIO()
    logger.info("have a string buffer")
    writer = csv.DictWriter(buffer, fieldnames, extrasaction='ignore')
    for order in pumpkinstore:
        if order["type"] == "pumpkin order":
            logger.info(order)
            writer.writerow(order)

    logger.info("pushing to the blob")
    outputblob.set(buffer.getvalue())
    logger.info("blob pushed")
    buffer.close()
    omap = dict()
    omap['status'] = 'ok'
    return func.HttpResponse(body=json.dumps(omap), status_code=200)
