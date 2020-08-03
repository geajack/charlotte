class RouteTable:

    def __init__(self):
        self.routes = []
        self.context_processor_function = None

    def route(self, rule, *args, **kwargs):
        def decorator(function):
            self.routes.append(Route(rule, function.__name__, args, kwargs))
            return function
        return decorator

    def context_processor(self, function):
        self.context_processor_function = function
        return function

    def add_to_app(self, controller, app):
        for route in self.routes:
            route.add_to_app(controller, app)

        if self.context_processor_function is not None:
            bound_method = getattr(controller, self.context_processor_function.__name__)
            app.context_processor(bound_method)

class Route:

    def __init__(self, rule, function_name, args, kwargs):
        self.rule = rule
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs

    def add_to_app(self, controller, app):
        bound_method = getattr(controller, self.function_name)
        app.add_url_rule(
            self.rule,
            self.function_name,
            bound_method,
            *self.args,
            **self.kwargs
        )