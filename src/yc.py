from typing import TypedDict, Literal


class Event(TypedDict):
    """
    https://cloud.yandex.ru/docs/functions/concepts/function-invoke#request
    """
    body: str
    httpMethod: Literal['POST', 'OPTIONS']


class Resp(TypedDict, total=False):
    """
    https://cloud.yandex.ru/docs/functions/concepts/function-invoke#response
    """
    statusCode: Literal[200]
    body: str
    headers: dict


def resp_cors() -> Resp:
    return {
        'statusCode': 200,
        'body': '',
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        }
    }
