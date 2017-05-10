class JsonRpcError(Exception):
    """
    Generic JSON RPC error
    """


class JsonRpcInvalidRequestError(JsonRpcError):
    """
    Invalid JSON RPC request was received. This can be caused by:

    - wrong content type
    """
