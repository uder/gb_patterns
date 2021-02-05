from urllib.parse import urlparse, parse_qs

def get_request_data(windy,request,environ):
    request['method'] = environ.get('REQUEST_METHOD')
    if environ.get('REQUEST_METHOD')=="GET":
        request['data']=parse_qs(environ.get('QUERY_STRING'))

    return request

