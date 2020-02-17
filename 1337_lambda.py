import boto3
import json
import time
import decimal
import os
from botocore.vendored import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


print('Loading function')

DYNAMO_DB = boto3.resource('dynamodb')
TABLE = DYNAMO_DB.Table('JoaogTestLambdaDB')

def lambda_handler(event, context):

    response_code = 200
    response_body = ""
    
    event.get("httpMethod")

    method = event.get("httpMethod")
    
    if method == None:
        response_code = 400
        response_body = "400 - BAD REQUEST"
    elif method == "POST":
        response_code,response_body = translate_text(event.get("body"))

    response = {
        "statusCode": response_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": response_body
    }

    return {"statusCode": response_code}

def translate_text(request_body):
    
    if request_body == None:
        return 400,"400 - BAD REQUEST" 
        
    request_body = json.loads(request_body)
    
    text = str(request_body['message']['text'])
    chat_id = request_body["message"]["chat"]["id"]

    if "/1337" in text:
        original = text.replace("/1337","")
        translated = original.translate(original.maketrans("abetisoABETISO", "48371504837150"))
    elif "/leet" in text:
        original = text.replace("/leet","")
        translated = original.translate(original.maketrans("48371504837150","abetisoABETISO"))

    TABLE.put_item(
        Item={
            'id':int(time.time()),
            'original_text':original,
            'translated_text':translated
        }
    )

    answer_json = {
        "chat_id":chat_id,
        "text":translated
    }
    
    url = BASE_URL + "/sendMessage"
    requests.post(url,answer_json)
    
    return 200,answer_json