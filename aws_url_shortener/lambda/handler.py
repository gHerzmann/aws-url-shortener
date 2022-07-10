import datetime
import json
import logging
import os
import time

import boto3
import shortuuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.resource("dynamodb")
table = client.Table(os.environ.get("TABLE_NAME"))


def save_url(target_url):
    week = datetime.datetime.today() + datetime.timedelta(days=7)
    expdate = int(time.mktime(week.timetuple()))
    short_id = shortuuid.uuid(name="example.com")[:6]
    table.put_item(Item={"id": short_id, "target_url": target_url, "expdate": expdate})
    return short_id


def get_url(short_id):
    item_result = table.get_item(Key={"id": short_id}, ConsistentRead=True)
    if "Item" in item_result:
        return item_result["Item"]["target_url"]


def create_short_url(event):
    query_string_params = event.get("queryStringParameters", None)
    if query_string_params:
        target_url = query_string_params.get("targetUrl", None)
        if target_url:
            short_id = save_url(target_url)
            short_url = (
                f"https://{event['requestContext']['domainName']}/prod/s/{short_id}"
            )
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "text/plain"},
                "body": f"Created URL: {short_url}",
            }


def retrieve_long_url(event):
    path_params = event.get("pathParameters", None)
    if path_params:
        short_id = path_params.get("short_id", None)
        if short_id:
            target_url = get_url(short_id)
            return {"statusCode": 301, "headers": {"Location": target_url}}


def main(event, context):
    logger.info("EVENT: " + json.dumps(event))
    if event["resource"] == "/create":
        return create_short_url(event)
    elif event["resource"] == "/s/{short_id}":
        return retrieve_long_url(event)
    return {"statusCode": 200, "body": "usage: ?targetUrl=URL"}
