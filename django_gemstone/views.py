from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_gemstone.decorators import methods


class JsonRpcEndpoint(View):
    def post(self, request):
        if request.content_type not in ("application/json",):
            return HttpResponseBadRequest("Invalid content type")
        return JsonResponse({"result": methods.get_method_names()})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(JsonRpcEndpoint, self).dispatch(request, *args, **kwargs)
