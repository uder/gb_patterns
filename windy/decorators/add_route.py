def add_route(url):
    def inner(view):
       print(f"decorator {url}")
       routes.append({"path": url, "handler": func})

       # def wrapper(windy,environ,start_response,request):
       #     result=view(windy,environ,start_response,request)
       #     return result

       # return wrapper
       return view
    return inner
