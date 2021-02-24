import os
import windy.views
import windy.middleware
import windy.templates
from windy.models.logger import WindyLogger
# from windy.db.connection import create_connection
# from windy.db.schema import DbInit
import windy.db
# from windy.include_patterns.unit_of_work import UnitOfWork
import windy.include_patterns.unit_of_work
import windy.db.mappers

from .router import Router

from pprint import pprint

class Windy():
	def __init__(self):
		self._init_router()
		self.drop_if_exists=False
		self.connection=windy.db.connection.create_connection()
		self.mapper=self._init_mapper()
		self._init_db()

		windy.include_patterns.unit_of_work.UnitOfWork.set_current(self.mapper,self.connection)
		self.unit_of_work=windy.include_patterns.unit_of_work.UnitOfWork.get_current()

		self._load_from_db()

		self.confdir=self._get_config_dir_path()
		self.middleware_fuctions=self.load_middleware()

		self.render=templates.render
		self.logger=WindyLogger()
		
		self.http_200='200 OK'
		self.http_404='404 NOT FOUND'
		self.response_headers=[('Content-type', 'text/html')]

	def _init_db(self):
		dbinit=windy.db.schema.DbInit(self.connection,self.drop_if_exists)
		dbinit.create_tables()

		return dbinit

	def _init_router(self):
		self.router=Router()
		self.router.init_routes()

	def _init_mapper(self):
		mapper=windy.db.mappers.Mapper
		mapper.register_mappers()
		return mapper

	def _load_from_db(self):
		for mapperclass in self.mapper.mappers.values():
			mapper=mapperclass(self.connection)
			mapper.load_from_db()

	def load_middleware(self):
		return middleware.import_functions()
		
	def _get_config_dir_path(self):
		dirname = os.path.abspath(os.path.dirname(__file__))
		confdir=os.path.join(dirname,"conf")
		return confdir
		
	def get_view(self,path):

		view=self.router.get_view(path)
		return view

	def __call__(self,environ,start_response):
		request={}
		request=middleware.invoke(self,request,environ)
		view=self.get_view(environ['PATH_INFO'])
		code,text=view(self,request)
		start_response(code, [('Content-Type', 'text/html')])
		return [text.encode('utf-8')]


class MockWindy(Windy):
	def __call__(self,environ,start_response):
		start_response('200 OK', [('Content-Type', 'text/html')])
		return [b'Hello from Mock']

class DebugWindy(Windy):
	def __call__(self,environ,start_response):
		self.logger.log('DEBUG','debug',str(environ))
		request={}
		request=middleware.invoke(self,request,environ)
		handler=self.get_view(environ['PATH_INFO'])
		retval=handler(self,environ,start_response,request)
		return retval
