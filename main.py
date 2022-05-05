import json

from src.models import Req


def handler(event, context):
    """
    https://functions.yandexcloud.net/d4evjj6ajnla3qrutemd
    :param event:
    :param context:
    :return:
    """
    body = json.loads(event['body'])
    req = Req(**body)

    return {
        'statusCode': 200,
        'body': req.apply()
    }
