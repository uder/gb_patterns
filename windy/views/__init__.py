import windy.db
from pprint import pprint
from windy.models.user import User
from windy.models.category import Category
from windy.models.course import Course
from windy.decorators.debug import debug
from windy.router import Router
from windy.cbv import ListView,CreateView
from windy.include_patterns.unit_of_work import UnitOfWork

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

@Router.add_route('/create-user/')
class CreateUser(CreateView):
	template = "create_user.html"
	def get_context(self,request):
		if request['method'] == 'POST':
			user_name = request['data'].get('user_name', "Anonymous")
			user_role = request['data'].get('user_role')
			user_course = request['data'].get('course_add',None)
			course = Course.get_course_by_name(user_course)
			if course or user_course is None:
				user = User.create(user_name, user_role)
				user.sign(course)
				self.notify(f'New user {repr(user)}')
			else:
				request['err'] = "No such course. Try again"
		return request


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
				category.mark_new()
				UnitOfWork.get_current().commit()
				if parent_name:
					parent.append(category)
				self.notify(f'New category - {repr(category)}')
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
				self.notify(f'New course - {repr(course)}')
			else:
				request['err'] = "No such category. Try again"
		return request

class ModifyCourse(CreateView):
	template = "modify_course.html"
	def get_context(self,request):
		if request['method'] == 'POST':
			name = request['data'].get('course_name', None)
			new_name = request['data'].get('new_course_name', None)
			new_duration = request['data'].get('new_course_duration', None)
			new_category_name = request['data'].get('new_course_category', None)
			remove_category_name = request['data'].get('remove_course_category', None)
			course = Course.get_course_by_name(name)
			new_category = Category.get_category_by_name(new_category_name)
			remove_category = Category.get_category_by_name(remove_category_name)
			if course:
				if new_name:
					if not course.set_name(new_name):
						request['err'] = f"Course {new_name} already exists. Try again"
				if new_duration:
					course.set_duration(new_duration)
				if new_category:
					new_category.append(course)
				if remove_category:
					remove_category.remove(course)

				message=f'Modify course - {repr(course)}'
				self.notify(message)
				for user in User.user_list_by_course(course):
					user.notify(message)
			else:
				request['err'] = "No such course. Try again"
		return request

class ModifyUser(CreateView):
	template = "modify_user.html"
	def get_context(self,request):
		if request['method'] == 'POST':
			user_name = request['data'].get('user_name',None)
			# user_role = request['data'].get('user_role')
			user_course_add = request['data'].get('course_add',None)
			user_course_del = request['data'].get('course_del',None)
			user=User.users.get(user_name,None)
			course_add=Course.courses.get(user_course_add,None)
			course_del=Course.courses.get(user_course_del,None)
			if user:
				if user_course_add:
					user.sign(course_add)
				if user_course_del:
					user.unsign(course_del)
				self.notify(f'Modify user {repr(user)}')
			else:
				request['err'] = "No such user. Try again"
		return request


# @Router.add_route('/debug/')
# @debug
# def root(windy,request):
# 	courses_list=Course.get_courses_list()
# 	request.update({'courses_list':courses_list})
# 	text=windy.render('index.html', **request)
# 	return '200', text

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

# def create_course(windy,request):
# 	if request['method']=='POST':
# 		name=request['data'].get('course_name', "NO_CRS_PATCH")
# 		duration=request['data'].get('course_duration',"100h")
# 		category_name=request['data'].get('course_category','')
# 		category = Category.get_category_by_name(category_name)
# 		if category:
# 			course = Course(name, duration)
# 			category.append(course)
# 			windy.logger.log('INFO', "learning", repr(course))
# 		else:
# 			request['err']="No such category. Try again"
#
# 	text=windy.render('create_course.html', **request)
# 	return '200', text



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

# def create_category(windy,request):
# 	if request['method']=='POST':
# 		name=request['data'].get('category_name', "NO_CAT_PATCH")
# 		desc=request['data'].get('category_desc',"No description")
# 		parent_name=request['data'].get('category_parent','')
# 		parent = Category.get_category_by_name(parent_name)
# 		if parent or parent_name=="":
# 			category = Category(name, desc)
# 			if parent_name:
# 				parent.append(category)
# 			windy.logger.log('INFO', "learning", repr(category))
# 		else:
# 			request['err']="No such category. Try again"
#
# 	text=windy.render('create_category.html', **request)
# 	return '200', text

# def category_list(windy,request):
# 	cat_list=Category.categories_list()
# 	request.update({'cat_list':cat_list})
#
# 	text=windy.render('category_list.html', **request)
# 	return '200', text

# def create_user(windy,request):
# 	if request['method'] == 'POST':
# 		user_name = request['data'].get('user_name', "Anonymous")
# 		user_role = request['data'].get('user_role')
#
# 		user = User.create(user_name, user_role)
# 		windy.logger.log('INFO',user_role,f'New user. Name: {user_name} Role: {user_role}')
#
# 	text = windy.render('create_user.html', **request)
# 	return '200', text

def not_found(windy,request):
	text=f"NOT EXISTENT PAGE"
	return '404', text
