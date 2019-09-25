import logging
from datetime import datetime
import azure.functions as func
import json
import csv
import uuid
import io


fieldnames = [
    "date","time", "deleted", "payment_type",
    "grand_count", "grand_total", "donation", "bake_sale",
    "total_pumpkin_count", "total_pumpkin_total", 
    "total_gourd_count", "total_gourd_total",
    "total_other_count", "total_other_total",
    "pumpkin_6_count", "pumpkin_6_total", "pumpkin_8_count", "pumpkin_8_total",
    "pumpkin_10_count", "pumpkin_10_total", "pumpkin_12_count", "pumpkin_12_total",
    "pumpkin_14_count", "pumpkin_14_total", "pumpkin_16_count", "pumpkin_16_total",
    "pumpkin_18_count", "pumpkin_18_total", "pumpkin_20_count", "pumpkin_20_total",
    "pumpkin_24_count", "pumpkin_24_total", "pumpkin_30_count", "pumpkin_30_total",
    "gourd_large_count", "gourd_large_total", "gourd_small_count", "gourd_small_total",
    "winged_large_count", "winged_large_total", "winged_small_count", "winged_small_total",
    "gizmo_count", "gizmo_total", "sticker_count", "sticker_total", 
    "candle_count", "candle_total", "spider_count", "spider_total", 
    "small_mum_count", "small_mum_total", "large_mum_count", "large_mum_total",
    "name", "phone", "timestamp"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(req: func.HttpRequest, pumpkinstore: func.DocumentList) -> func.HttpResponse:
    logger.info('Python HTTP trigger function processed a request.')

    start = float(req.params.get('start'))
    end = float(req.params.get('end'))
# SELECT * FROM c WHERE c.type='pumpkin order' ORDER BY c._ts
#
    buffer = io.StringIO()

    logger.info("have a string buffer")
    writer = csv.DictWriter(buffer, fieldnames, extrasaction='ignore')
    writer.writeheader()
    for order in pumpkinstore:
        if order.get('timestamp') is not None:
            order_time = float(order.get('timestamp'))
            if start == 0 or (start < order_time and order_time < end):
                if order["type"] == "pumpkin order":
                    logger.info(order)
                    writer.writerow(order)

    contents = buffer.getvalue()
    buffer.close()
    logger.info(contents)
    datestr = datetime.today().strftime('%Y-%m-%d') 
    logger.info(datestr)
    filename_to_be = f'inline; filename={datestr}.csv'
    logger.info(filename_to_be)
    header = dict()
    header['Content-Length'] = str(len(contents))
    header['Content-Disposition'] = filename_to_be
    logger.info(header)
    return func.HttpResponse(body=contents, status_code=200, headers=header, mimetype="test/csv")
