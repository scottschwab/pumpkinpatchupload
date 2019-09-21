import logging

import azure.functions as func
import json
import uuid


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate(body):
    missing = list()
    REQUIRED_FIELDS=["grand_total","donation"]
    for r in REQUIRED_FIELDS:
        if not r in body:
            missing.append(r)
    return missing


def main(req: func.HttpRequest, pumpkinstore: func.Out[func.Document]) -> func.HttpResponse:
    logger.info('Python HTTP trigger Storing in the pumpkin patch.')
    # z = dir(pumpkinstore)
    # logger.info(z)
    # load the body
    body = req.get_json()
    logger.info(body)
    missing = validate(body)
    # validate input
    if missing:
        eOut = dict()
        eOut["error"] = "missing values"
        eOut["missing"] = missing
        logger.warning("Missing " + missing)
        return func.HttpResponse(body=json.dumps(eOut), status_code=400)

    # generate a unique id, so we can remove the entry if needed
    uu = str(uuid.uuid1())
    logger.info(uu)
    # add the id to the content uploaded
    body["id"] = uu
    body["type"] = "pumpkin order"
    logger.info("trying to send to cosmosdb")
    # write to the db, in theory it returns a code, but it is always None
    pumpkinstore.set(func.Document.from_dict(body))
    omap = dict()
    # generate the output 
    omap["id"] = uu
    logger.info(json.dumps(omap))
    return func.HttpResponse(body=json.dumps(omap), status_code=201)
