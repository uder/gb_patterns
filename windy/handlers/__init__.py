from pprint import pprint
from windy.models.user import User
from windy.models.category import Category
from windy.models.course import Course

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

		windy.logger.log('INFO', "feedback", f'We have received Feedback from: "{name}" with return mail: "{email}" with subject: "{subject}" and message: "{message}"')

	html=windy.render('feedback.html', **request).encode('utf-8')
	return [html]

def create_course(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	if request['method']=='POST':
		name=request['data'].get('course_name', "NO_CRS_PATCH")
		duration=request['data'].get('course_duration',"100h")

		course=Course(name,duration)
		windy.logger.log('INFO', "learning", repr(course))

	html=windy.render('create_course.html', **request).encode('utf-8')
	return [html]

def create_category(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	if request['method']=='POST':
		name=request['data'].get('category_name', "NO_CAT_PATCH")
		desc=request['data'].get('category_desc',"No description")

		category=Category(name,desc)
		windy.logger.log('INFO', "learning", repr(category))

	html=windy.render('create_category.html', **request).encode('utf-8')
	return [html]

def category_list(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	html=windy.render('category_list.html', **request).encode('utf-8')
	return [html]

def create_user(windy,environ,start_response,request):
	start_response(windy.http_200, windy.response_headers)
	if request['method'] == 'POST':
		user_name = request['data'].get('user_name', "Anonymous")
		user_role = request['data'].get('user_role')

		#user=windy.models.User.create(user_name,user_role)
		user = User.create(user_name, user_role)
		#user.say()
		windy.logger.log('INFO',user_role,f'New user. Name: {user_name} Role: {user_role}')

		#print("---")
		##print(f'New {user_role} have joined. {user_role}\'s name is {user_name}')
		#print("---")

	html = windy.render('create_user.html', **request).encode('utf-8')
	return [html]

def not_found(windy,environ,start_response,request):
	start_response(windy.http_404, windy.response_headers)
	return [b'NOT EXISTENT PAGE '+environ['PATH_INFO'].encode('utf-8')]