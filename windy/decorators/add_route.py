def add_route(url):
    def decorator(view):
        def wrapper(windy,environ,start_response,request):
            windy.routes.append({"path": url, "handler": view.__name__})
            result=view(windy,environ,start_response,request)
            return result

        return wrapper
    return decorator
