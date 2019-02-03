from charlotte.renderers import mathdown, plain

def get_renderer(format):
    if format == "mathdown":
        return mathdown
    elif format == "plain":
        return plain
    else:
        return None