import json

from src.models import Req, Event, Resp


def handler(event: Event, context) -> Resp:
    """
    https://functions.yandexcloud.net/d4evjj6ajnla3qrutemd
    :param event:
    :param context:
    :return:
    """
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'body': '',
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            }
        }

    body = json.loads(event['body'])
    req = Req(**body)

    return {
        'statusCode': 200,
        'body': req.apply()
    }
