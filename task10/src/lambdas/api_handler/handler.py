import os

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
        reservations_table = os.environ['RESERVATIONS_TABLE']
        tables_table = os.environ['TABLES_TABLE']
        user_pool_name = os.environ['USER_POOL']
        _LOG.info(f"{reservations_table=}")
        _LOG.info(f"{tables_table=}")
        _LOG.info(f"{user_pool_name=}")
        return {"event": event}
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
