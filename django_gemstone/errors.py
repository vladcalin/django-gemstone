class JsonRpcError(Exception):
    """
    Generic JSON RPC error
    """


class JsonRpcInvalidRequestError(JsonRpcError):
    """
    Invalid JSON RPC request was received. This can be caused by:

    - wrong content type
    - invalid JSON body
    - body not respecting the JSON RPC 2.0 specs
    """
    code = -32600


class JsonRpcMethodNotFoundError(JsonRpcError):
    """The requested method is not found"""
    code = 32601


class JsonRpcParseError(JsonRpcError):
    """No valid JSON could be decoded from the request body"""
    code = -32700


class JsonRpcInvalidParamsError(JsonRpcError):
    """Invalid params"""
    code = -32602


class JsonRpcInternalError(JsonRpcError):
    """Internal error"""
    code = -32603

    def __init__(self, cause_exc):
        self.exc = cause_exc
