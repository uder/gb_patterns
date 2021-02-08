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
	if request['method']=='POST':
		name=request['data'].get('name',"Anonymous")
		email=request['data'].get('email',"Without Mail")
		subject=request['data'].get('subject','Without Subject')
		message=request['data'].get('message','Empty Message')

		print("---")
		print(f'We have received Feedback from: "{name}" with return mail: "{email}" with subject: "{subject}" and message: "{message}"')
		print("---")

	html=windy.render('feedback.html', **request).encode('utf-8')
	return [html]

def create_course(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('create_course.html', **request).encode('utf-8')
	return [html]

def create_category(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('create_category.html', **request).encode('utf-8')
	return [html]

def category_list(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('category_list.html', **request).encode('utf-8')
	return [html]


def not_found(windy,environ,start_response,request):
	start_response(windy.http_404, windy.response_headers)
	return [b'NOT EXISTENT PAGE '+environ['PATH_INFO'].encode('utf-8')]