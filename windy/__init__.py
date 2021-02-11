import json 
import os
import windy.handlers
import windy.middleware
import windy.templates
from windy.models.logger import WindyLogger

from pprint import pprint

class Windy():
	def __init__(self):
		self.confdir=self._get_config_dir_path()
		self.routes=self.get_routes()
		self.middleware_fuctions=self.load_middleware()

		self.render=templates.render
		self.logger=WindyLogger()
		
		self.http_200='200 OK'
		self.http_404='404 NOT FOUND'
		self.response_headers=[('Content-type', 'text/html')]
		self.default='not_found'
	
	def load_middleware(self):
		return middleware.import_functions()
		
	def _get_config_dir_path(self):
		dirname = os.path.abspath(os.path.dirname(__file__))
		confdir=os.path.join(dirname,"conf")
		return confdir
		
	def get_routes(self):
		dirname = os.path.dirname(__file__)
		config_file = os.path.join(dirname, "conf/routes.json")
		json_conf=""
		with open(config_file,"r") as f:
			json_conf=json.load(f)
		return json_conf
		
	def get_handler(self,path):
		handler=self.default
		for obj in self.routes:
			if path==obj['path']:
				handler=obj['handler']
				
		func=getattr(windy.handlers,handler)
		return func
		
	def __call__(self,environ,start_response):
		request={}
		request=middleware.invoke(self,request,environ)
		handler=self.get_handler(environ['PATH_INFO'])
		retval=handler(self,environ,start_response,request)
		return retval
