import dataclasses
from ast import literal_eval
from typing import Literal, TypedDict, Optional

from src.tools import dict_to_json


@dataclasses.dataclass
class Req:
    tool: Literal['json_tool']
    dict: str

    def apply(self) -> str:
        if self.tool == 'dict_to_json':
            return dict_to_json(literal_eval(self.dict))


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
