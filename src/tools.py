import json


def dict_to_json(dict_: dict) -> str:
    return json.dumps(dict_, indent=2)
