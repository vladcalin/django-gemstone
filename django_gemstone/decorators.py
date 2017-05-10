class ExposedMethod(object):
    def __init__(self, name, callable_):
        self.name = name
        self.callable = callable_

    def call_with_params(self, params):
        if isinstance(params, (list, tuple)):
            return self.callable(*params)
        elif isinstance(params, dict):
            return self.callable(**params)


class ExposedMethodContainer(object):
    def __init__(self):
        self.methods = {}

    def add_method(self, exposed_method_obj: ExposedMethod):
        self.methods[exposed_method_obj.name] = exposed_method_obj

    def get_method_by_name(self, name):
        method = self.methods.get(name)
        if not method:
            raise ValueError("No method named '{}' found".format(name))
        return method

    def get_method_names(self):
        return list(self.methods.keys())


methods = ExposedMethodContainer()


def exposed_method(name=None):
    def decorator(func):
        nonlocal name
        if not name:
            name = func.__name__
        methods.add_method(ExposedMethod(name, func))
        return func

    return decorator
