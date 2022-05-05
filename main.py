import json

from src.models import Req
from src.yc import Event, Resp, resp_cors


def handler(event: Event, context) -> Resp:
    """
    https://functions.yandexcloud.net/d4evjj6ajnla3qrutemd
    :param event:
    :param context:
    :return:
    """
    if event['httpMethod'] == 'OPTIONS':
        return resp_cors()

    body = json.loads(event['body'])
    req = Req(**body)

    return {
        'statusCode': 200,
        'body': req.apply()
    }
