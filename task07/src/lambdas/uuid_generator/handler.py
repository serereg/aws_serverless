import json
from datetime import datetime
from uuid import uuid4

import boto3

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('UuidGenerator-handler')


class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # event={
        #         'version': '0', 'id': 'a3441b5a-dc44-2028-58a6-608c8b8b816a', 'detail-type': 'Scheduled Event', 
        #         'source': 'aws.events', 'account': '905418349556', 'time': '2024-05-08T11:33:44Z', 'region': 'eu-central-1', 
        #         'resources': ['arn:aws:events:eu-central-1:905418349556:rule/cmtr-9766e57a-uuid_trigger'], 
        #         'detail': {}
        # }

        _LOG.info(f"{event=}")
        s3 = boto3.resource('s3')
        bucket_name = 'cmtr-9766e57a-uuid-storage-test'
        file_name = f"{datetime.now().isoformat()}Z"
        record = {"ids": [str(uuid4()) for _ in range(10)]}
        content = json.dumps(record)
        _LOG.info(f"{content=}")
        s3.Object(bucket_name, file_name).put(Body=content)
        return 200
    

HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
