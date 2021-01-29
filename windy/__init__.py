import json 
import os
import windy.handlers
import windy.middleware

from pprint import pprint

class Windy():
	def __init__(self):
		self.routes=self.get_routes()
		self.middleware_fuctions=self.load_middleware()

		self.http_200='200 OK'
		self.http_404='404 NOT FOUND'
		self.response_headers=[('Content-type', 'text/plain')]
		self.default='not_found'
	
	def load_middleware(self):
		return middleware.import_functions()
		
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
		# path=environ['PATH_INFO']
		request={}
		request=middleware.invoke(self,request,environ)
		pprint(request)
		handler=self.get_handler(environ['PATH_INFO'])
		retval=handler(self,environ,start_response)
		return retval
