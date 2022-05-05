import dataclasses
from ast import literal_eval
from typing import Literal

from src.tools import dict_to_json


@dataclasses.dataclass
class Req:
    tool: Literal['json_tool']
    dict: str

    def apply(self) -> str:
        if self.tool == 'dict_to_json':
            return dict_to_json(literal_eval(self.dict))
