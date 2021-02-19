from pprint import pprint
from windy.models.user import User
from windy.models.category import Category
from windy.models.course import Course
from windy.decorators.debug import debug
from windy.router import Router
from windy.cbv import ListView,CreateView

@Router.add_route('/cat/')
class ListCategory(ListView):
	template = "category_list.html"
	def get_context(self,request):
		context={}
		context.update({'cat_list': Category.categories_list()})
		return context

@Router.add_route('/list/')
@debug
class ListCourse(ListView):
	template = "index.html"
	def get_context(self,request):
		context={}
		context.update({'courses_list': Course.get_courses_list()})
		return context

@Router.add_route('/test/')
class CreateCategory(CreateView):
	template = "create_category.html"
	def get_context(self,request):
		if request['method'] == 'POST':
			name = request['data'].get('category_name', "NO_CAT_PATCH")
			desc = request['data'].get('category_desc', "No description")
			parent_name = request['data'].get('category_parent', '')
			parent = Category.get_category_by_name(parent_name)
			if parent or parent_name == "":
				category = Category(name, desc)
				if parent_name:
					parent.append(category)
				# windy.logger.log('INFO', "learning", repr(category))
			else:
				request['err'] = "No such category. Try again"
		return request

class CreateCourse(CreateView):
	template = "create_course.html"
	def get_context(self,request):
		if request['method'] == 'POST':
			name = request['data'].get('course_name', "NO_CRS_PATCH")
			duration = request['data'].get('course_duration', "100h")
			category_name = request['data'].get('course_category', '')
			category = Category.get_category_by_name(category_name)
			if category:
				course = Course(name, duration)
				category.append(course)
				# windy.logger.log('INFO', "learning", repr(course))
			else:
				request['err'] = "No such category. Try again"
		return request


@Router.add_route('/debug/')
@debug
def root(windy,request):
	courses_list=Course.get_courses_list()
	request.update({'courses_list':courses_list})
	text=windy.render('index.html', **request)
	return '200', text

def about(windy,request):
	text=windy.render('about.html', **request)
	return '200', text

def feedback(windy,request):
	if request['method']=='POST':
		name=request['data'].get('name',"Anonymous")
		email=request['data'].get('email',"Without Mail")
		subject=request['data'].get('subject','Without Subject')
		message=request['data'].get('message','Empty Message')

		windy.logger.log('INFO', "feedback", f'We have received Feedback from: "{name}" with return mail: "{email}" with subject: "{subject}" and message: "{message}"')

	text=windy.render('feedback.html', **request)
	return '200', text

def create_course(windy,request):
	if request['method']=='POST':
		name=request['data'].get('course_name', "NO_CRS_PATCH")
		duration=request['data'].get('course_duration',"100h")
		category_name=request['data'].get('course_category','')
		category = Category.get_category_by_name(category_name)
		if category:
			course = Course(name, duration)
			category.append(course)
			windy.logger.log('INFO', "learning", repr(course))
		else:
			request['err']="No such category. Try again"

	text=windy.render('create_course.html', **request)
	return '200', text



def copy_course(windy,request):
	if request['method']=='POST':
		name=request['data'].get('course_name', "NO_CRS_PATCH")
		copy_from=request['data'].get('course_copy_from',"NO_CRS_PATCH")

		source_course=Course.get_course_by_name(copy_from)
		if source_course:
			course=source_course.clone()
			if course.set_name(name):
				windy.logger.log('INFO', "learning", repr(course))
			else:
				windy.logger.log('ERROR', "learning", f'Cant set name  {name}')
		else:
			windy.logger.log('ERROR', "learning", f'No such course {copy_from}')



	text=windy.render('copy_course.html', **request)
	return '200', text

def create_category(windy,request):
	if request['method']=='POST':
		name=request['data'].get('category_name', "NO_CAT_PATCH")
		desc=request['data'].get('category_desc',"No description")
		parent_name=request['data'].get('category_parent','')
		parent = Category.get_category_by_name(parent_name)
		if parent or parent_name=="":
			category = Category(name, desc)
			if parent_name:
				parent.append(category)
			windy.logger.log('INFO', "learning", repr(category))
		else:
			request['err']="No such category. Try again"

	text=windy.render('create_category.html', **request)
	return '200', text

def category_list(windy,request):
	cat_list=Category.categories_list()
	request.update({'cat_list':cat_list})

	text=windy.render('category_list.html', **request)
	return '200', text

def create_user(windy,request):
	if request['method'] == 'POST':
		user_name = request['data'].get('user_name', "Anonymous")
		user_role = request['data'].get('user_role')

		user = User.create(user_name, user_role)
		windy.logger.log('INFO',user_role,f'New user. Name: {user_name} Role: {user_role}')

	text = windy.render('create_user.html', **request)
	return '200', text

def not_found(windy,request):
	text=f"NOT EXISTENT PAGE"
	return '404', text
