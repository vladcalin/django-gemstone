from django.shortcuts import render
from django_gemstone.decorators import exposed_method


# Create your views here.


@exposed_method()
def say_hello(name):
    return "Hello {}".format(name)
