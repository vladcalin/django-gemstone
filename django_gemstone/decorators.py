class ExposedMethod(object):
    def __init__(self, name, callable_):
        self.name = name
        self.callable = callable_


class ExposedMethodContainer(object):
    def __init__(self):
        self.methods = {}

    def add_method(self, method_callable):
        self.methods[method_callable.name] = method_callable

    def get_method(self, name):
        method = self.methods.get(name)
        if not method:
            raise ValueError("No method named '{}' found".format(name))
        return method

    def get_method_names(self):
        return list(self.methods.keys())


methods = ExposedMethodContainer()


def exposed_method(name=None, **kwargs):
    def decorator(func):
        if not name:
            name = func.__name__
        methods.add_method(ExposedMethod(name, func))

    return decorator
