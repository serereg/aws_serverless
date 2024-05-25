import json
import os
from uuid import uuid4

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info(f"{event=}")
        reservations_table_name = os.environ['RESERVATIONS_TABLE']
        tables_table_name = os.environ['TABLES_TABLE']
        user_pool_name = os.environ['USER_POOL']
        _LOG.info(f"{reservations_table_name=}")
        _LOG.info(f"{tables_table_name=}")
        _LOG.info(f"{user_pool_name=}")

        dynamodb = boto3.resource('dynamodb')
        tables_table = dynamodb.Table(tables_table_name)
        reservations_table = dynamodb.Table(reservations_table_name)
        try:
            if event['path'] == '/signup' and event['httpMethod'] == 'POST':
                _LOG.info("signup post")
                body = json.loads(event['body'])

                first_name = body['firstName']
                last_name = body['lastName']
                email = body['email']
                password = body['password']

                client = boto3.client('cognito-idp')

                user_pool_name = os.environ['USER_POOL']
                _LOG.info(f'{user_pool_name=}')

                response = client.list_user_pools(MaxResults=60)
                user_pool_id = None
                for user_pool in response['UserPools']:
                    if user_pool['Name'] == user_pool_name:
                        user_pool_id = user_pool['Id']
                        break
                _LOG.info(f'{user_pool_id=}')

                app_client_id = None
                response = client.list_user_pool_clients(UserPoolId=user_pool_id)
                _LOG.info(f"{response=}")
                for app_client in response['UserPoolClients']:
                    if app_client['ClientName'] == "client_app":
                        app_client_id = app_client['ClientId']
                _LOG.info(f'{app_client_id =}')

                response = client.sign_up(ClientId=app_client_id, 
                                          Username=first_name, 
                                          Password=password, 
                                          UserAttributes=[{"Name": "email", "Value": email }]
                                          )
                _LOG.info(f'{response =}')


            elif event['path'] == '/signin' and event['httpMethod'] == 'POST':
                _LOG.info("signip post")

            elif event['path'] == '/tables' and event['httpMethod'] == 'POST':
                _LOG.info("tables post")
                item = json.loads(event['body'])
                response = tables_table.put_item(Item=item)
                _LOG.info(response)
                return {"statusCode": 200, 
                        "body": json.dumps({"id": item["id"]})
                        }

            elif event['path'] == '/tables' and event['httpMethod'] == 'GET':
                response = tables_table.scan()
                items = response['Items']
                _LOG.info(items)
                return {"statusCode": 200, "body": json.dumps(items)}

            elif event['resource'] == '/tables/{tableId}' and event['httpMethod'] == 'GET':
                table_id = int(event['path'].split('/')[-1])
                _LOG.info(f"{table_id=}")
                
            elif event['path'] == '/reservations' and event['httpMethod'] == 'POST':
                _LOG.info("reservations post")
                item = json.loads(event['body'])
                reservation_id = uuid4()
                response = reservations_table.put_item(Item={"id": reservation_id, **item})
                _LOG.info(response)
                return {"statusCode": 200, 
                        "body": json.dumps({"reservationId": reservation_id})
                        }

            elif event['path'] == '/reservations' and event['httpMethod'] == 'GET':
                _LOG.info("reservations get")
                response = reservations_table.scan()
                items = response['Items']
                _LOG.info(items)
                return {"statusCode": 200, "body": json.dumps(items)}

            else:
                raise KeyError("no method")
        except Exception as e:
            _LOG.info('Bad request')
            _LOG.info(f'Error: {e}')

            message = {
                'statusCode': 400,
                'body': json.dumps({
                    'statusCode': 400,
                    'error': 'Bad request',
                    'message': f'{e}'
                })
            }

            _LOG.info(f'{message=}')
            return message
        return {"statusCode": 200, "body": json.dumps(event)}
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
