from urllib.parse import urlparse, parse_qs

def _parse_request_string(string):
    data={}
    parse_dict=parse_qs(string)
    for key in parse_dict:
        data.update({key:parse_dict[key][0]})

    return data


def get_request_data(windy,request,environ):
    request['method'] = environ.get('REQUEST_METHOD')
    data_str=""
    if environ.get('REQUEST_METHOD')=="GET":
        data_str=environ.get('QUERY_STRING',"")
    elif environ.get('REQUEST_METHOD')=="POST":
        content_length=int(environ.get('CONTENT_LENGTH','0'))
        if content_length>0:
            data_str=environ['wsgi.input'].read(content_length).decode('utf-8')
        else:
            data_str=""

    request['data']=_parse_request_string(data_str)

    return request

