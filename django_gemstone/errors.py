class JsonRpcError(Exception):
    """
    Generic JSON RPC error
    """
    code = None
    message = None

    def __init__(self, request_id=None):
        self.id = request_id

    def as_jsonrpc_response(self):
        resp = {
            "jsonrpc": "2.0",
            "result": None,
            "error": {
                "code": self.code,
                "message": self.message
            }
        }
        if self.id:
            resp["id"] = self.id
        return resp


class JsonRpcInvalidRequestError(JsonRpcError):
    """
    Invalid JSON RPC request was received. This can be caused by:

    - wrong content type
    - invalid JSON body
    - body not respecting the JSON RPC 2.0 specs
    """
    message = "Invalid request"
    code = -32600


class JsonRpcMethodNotFoundError(JsonRpcError):
    """The requested method is not found"""
    message = "Method not found"
    code = -32601


class JsonRpcParseError(JsonRpcError):
    """No valid JSON could be decoded from the request body"""
    message = "Parse error"
    code = -32700


class JsonRpcInvalidParamsError(JsonRpcError):
    """Invalid params"""
    message = "Invalid params"
    code = -32602


class JsonRpcInternalError(JsonRpcError):
    """Internal error"""
    message = "Internal error"
    code = -32603

    def __init__(self, cause_exc, request_id):
        self.exc = cause_exc
        super(JsonRpcInternalError, self).__init__(request_id)

    def as_jsonrpc_response(self, id=None):
        resp = super(JsonRpcInternalError, self).as_jsonrpc_response()
        resp["error"]["info"] = {
            "class": type(self.exc).__name__,
            "message": str(self.exc)
        }
        return resp
