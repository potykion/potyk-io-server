from src.models import Req


def test_Req():
    assert Req(**{"tool": "dict_to_json", "dict": "{'httpMethod': 'GET'}"}).apply() == \
           '{\n  "httpMethod": "GET"\n}'
