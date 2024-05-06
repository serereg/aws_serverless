import json
import uuid
import boto3
from datetime import datetime

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')

dynamodb = boto3.resource('dynamodb')
table_name = 'cmtr-9766e57a-Events'


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(event)

        record = {}
        record["id"] = str(uuid.uuid4())
        record["principalId"] = event["principalId"]
        record["createdAt"] = datetime.utcnow().isoformat()
        record["body"] = event["content"]
        _LOG.info(record)

        table = dynamodb.Table(table_name)
        table.put_item(Item=record)

        return {
                "statusCode": 200,
                "body": json.dumps(record)
                }
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
