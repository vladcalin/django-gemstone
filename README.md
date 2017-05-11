# django-gemstone
JSONRPC microservices with Django


Quick example usage:

- include "django_gemstone" in INSTALLED_APPS
- create ``methods.py`` in any installed app
- in ``methods.py`` write the exposed methods 

```
from django_gemstone.decorators import exposed_method

@exposed_method()
def say_hello(name):
    return "Hello {}".format(name)
  
```

- in urls, include the following

```
from django_gemstone import views
# ...
urlpatterns = [
  # ...
  url(r'^api', views.JsonRpcEndpoint.as_view())
]
```

- start the project (``python manage.py runserver 8000``)
- make a POST request to http://localhost:8000/api with the content

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "say_hello",
  "params": {
    "name": "world"
  }
}
```

The response should be

```
{
  "id": 1,
  "jsonrpc": "2.0",
  "error": null,
  "result": "hello world"
}
```
