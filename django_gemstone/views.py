from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .decorators import methods
from .jsonrpc import get_jsonrpc_request_from_http_request
from .errors import JsonRpcInvalidRequestError, JsonRpcParseError, JsonRpcInternalError, JsonRpcInvalidParamsError, \
    JsonRpcMethodNotFoundError, JsonRpcError


class JsonRpcEndpoint(View):
    """
    The main view class for the JSON RPC endpoint.
    """

    def post(self, request):
        # checks the content type
        if request.content_type not in ("application/json",):
            raise JsonRpcInvalidRequestError()

        # parse the request
        jsonrpc_req = get_jsonrpc_request_from_http_request(request)

        # check if the method exists
        try:
            method_obj = methods.get_method_by_name(jsonrpc_req.method)
        except ValueError:
            raise JsonRpcMethodNotFoundError(jsonrpc_req.id)

        # actual method call
        try:
            resp = method_obj.call_with_params(jsonrpc_req.params)
        except Exception as e:
            raise JsonRpcInternalError(e)

        # return the json rpc response in case of success
        return JsonResponse({
            "jsonrpc": "2.0",
            "id": jsonrpc_req.id,
            "result": resp,
            "error": None
        })

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(JsonRpcEndpoint, self).dispatch(request, *args, **kwargs)
        except JsonRpcError as e:
            return JsonResponse(e.as_jsonrpc_response())
