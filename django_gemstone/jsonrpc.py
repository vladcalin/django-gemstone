import json

import jsonschema
from django import http

from .errors import JsonRpcError, JsonRpcInvalidRequestError, JsonRpcParseError


def get_jsonrpc_request_from_http_request(request):
    if not isinstance(request, http.HttpRequest):
        raise TypeError("Invalid type: expected django.http.HttpRequest but got {}".format(type(request).__name__))

    if request.content_type != "application/json":
        raise JsonRpcInvalidRequestError()

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        raise JsonRpcParseError()

    if isinstance(data, dict):
        return JsonRpcRequest.from_dict(data)
    elif isinstance(data, list):
        # TODO: Batch request
        raise NotImplementedError("Batch requests not yet supported")
    else:
        raise JsonRpcInvalidRequestError()


class JsonRpcRequest(object):
    schema = {
        "type": "object",
        "properties": {
            "jsonrpc": {
                "enum": ["2.0"]
            },
            "method": {
                "type": "string"
            },
            "params": {
                "type": ["array", "object"]
            },
            "id": {}
        },
        "required": ["jsonrpc", "method"]
    }

    def __init__(self, id=None, method=None, params=None):
        self.id = id
        self.method = method
        self.params = params

    @classmethod
    def from_dict(cls, d):
        if not isinstance(d, dict):
            raise TypeError("Invalid type: expected dict but got {}".format(type(d).__name__))

        try:
            jsonschema.validate(d, cls.schema)
        except jsonschema.ValidationError as e:
            raise ValueError("Invalid jsonrpc request: {0}".format(str(e)))

        return cls(d.get("id"), d["method"], d.get("params", {}))
