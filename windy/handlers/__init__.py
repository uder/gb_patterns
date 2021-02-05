def root(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('index.html', **request).encode('utf-8')
	return [html]
	
def about(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('about.html', **request).encode('utf-8')
	return [html]

def feedback(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('feedback.html', **request).encode('utf-8')
	return [html]

def not_found(windy,environ,start_response,request):
	start_response(windy.http_404, windy.response_headers)
	return [b'NOT EXISTENT PAGE '+environ['PATH_INFO'].encode('utf-8')]