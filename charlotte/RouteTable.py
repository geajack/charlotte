class RouteTable:

    def __init__(self):
        self.routes = []
        self.context_processor_function = None

    def route(self, rule, *args, **kwargs):
        def decorator(function):
            self.routes.append(Route([rule, None, function, *args], kwargs))
        return decorator

    def context_processor(self, function):
        self.context_processor_function = function

    def add_to_app(self, app):
        for route in self.routes:
            route.add_to_app(app)

        if self.context_processor_function is not None:
            app.context_processor(self.context_processor_function)

class Route:

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def add_to_app(self, app):
        app.add_url_rule(*self.args, **self.kwargs)