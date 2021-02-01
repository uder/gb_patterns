def root(windy,environ,start_response,request):
	author=request.get('author',None)
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('index.html', author=author).encode('utf-8')
	print(type(html))
	return [html]
	
def about(windy,environ,start_response,request):
	author=request.get('author',None)
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('about.html', author=author).encode('utf-8')
	return [html]
	
def not_found(windy,environ,start_response,request):
	start_response(windy.http_404, windy.response_headers)
	return [b'NOT EXISTENT PAGE '+environ['PATH_INFO'].encode('utf-8')]