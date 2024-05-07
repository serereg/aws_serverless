import json
import uuid
import boto3
from datetime import datetime

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('AuditProducer-handler')

dynamodb = boto3.resource('dynamodb')
table_configuration = 'cmtr-9766e57a-Configuration-test'
table_audit = 'cmtr-9766e57a-Audit-test'


class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(event)
        # {'Records': [{'eventID': '87f90b0e0af3a1fc04a8966b56083974', 'eventName': 'INSERT', 
        #                 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'eu-central-1', 
        #                 'dynamodb': {'ApproximateCreationDateTime': 1715027485.0, 
        #                              'Keys': {'key': {'S': 'asdf'}}, 
        #                              'NewImage': {'value': {'N': '1234'}, 'key': {'S': 'asdf'}}, 
        #                              'SequenceNumber': '2500000000026925944438', 'SizeBytes': 22, 
        #                              'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 
        #                 'eventSourceARN': 'arn:aws:dynamodb:eu-central-1:905418349556:table/cmtr-9766e57a-Configuration/stream/2024-05-06T20:26:53.544'}]}
        if event['Records'][0]['eventName'] == 'INSERT':
            record = {
                    "id": str(uuid.uuid4()),
                    "itemKey": event['Records'][0]['dynamodb']['Keys']['key']['S'],
                    "modificationTime": datetime.utcnow().isoformat(),
                    "newValue": {
                        "key": event['Records'][0]['dynamodb']['NewImage']['key']['S'],
                        "value": int(event['Records'][0]['dynamodb']['NewImage']['value']['N'])
                        }
                    }
        # {'Records': [{'eventID': '2711017d141aa1b35c3a11f0fe973ce0', 'eventName': 'MODIFY', 
        #                 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'eu-central-1', 
        #                 'dynamodb': {'ApproximateCreationDateTime': 1715027498.0, 
        #                              'Keys': {'key': {'S': 'asdf'}}, 
        #                              'NewImage': {'value': {'N': '5678'}, 'key': {'S': 'asdf'}}, 
        #                              'OldImage': {'value': {'N': '1234'}, 'key': {'S': 'asdf'}}, 
        #                              'SequenceNumber': '2600000000026925951902', 'SizeBytes': 37, 
        #                              'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 
        #                 'eventSourceARN': 'arn:aws:dynamodb:eu-central-1:905418349556:table/cmtr-9766e57a-Configuration/stream/2024-05-06T20:26:53.544'}]}
        elif event['Records'][0]['eventName'] == 'MODIFY':
            record = {
                    "id": str(uuid.uuid4()),
                    "itemKey": event['Records'][0]['dynamodb']['Keys']['key']['S'],
                    "modificationTime": datetime.utcnow().isoformat(),
                    "updatedAttribute": "value",
                    "oldValue": int(event['Records'][0]['dynamodb']['OldImage']['value']['N']),
                    "newValue": int(event['Records'][0]['dynamodb']['NewImage']['value']['N'])
                    }
        else:
            record = {}

        _LOG.info(record)

        table = dynamodb.Table(table_audit)
        table.put_item(Item=record)

        return {
                "statusCode": 200,
                "body": json.dumps(record)
                }
    

HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
