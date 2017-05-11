from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .decorators import methods
from .jsonrpc import get_jsonrpc_request_from_http_request
from .errors import JsonRpcMethodNotFoundError, JsonRpcInternalError


class JsonRpcEndpoint(View):
    def post(self, request):
        if request.content_type not in ("application/json",):
            return HttpResponseBadRequest("Invalid content type")

        jsonrpc_req = get_jsonrpc_request_from_http_request(request)

        try:
            method_obj = methods.get_method_by_name(jsonrpc_req.method)
        except ValueError:
            raise JsonRpcMethodNotFoundError("Method '{}' not found".format(jsonrpc_req.method))

        try:
            resp = method_obj.call_with_params(jsonrpc_req.params)
        except Exception as e:
            raise JsonRpcInternalError(e)

        return JsonResponse({
            "jsonrpc": "2.0",
            "id": jsonrpc_req.id,
            "result": resp,
            "error": None
        })

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(JsonRpcEndpoint, self).dispatch(request, *args, **kwargs)
