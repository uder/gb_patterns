import os
import sys
from importlib import import_module
from pprint import pprint

def import_functions():
	path=os.path.dirname(__file__)
	func_files=os.listdir(path)
	func_list=[]
	for f in func_files:
		if not f.startswith("_") and f.endswith(".py"):
			file=os.path.join(path,f)
			m=import_module ("."+f[:-3],package=__name__)
			funcs=_get_funcs(m)
			func_list.extend(funcs)
	return func_list
			
def _get_funcs(m):
	obj_list=dir(m)
	obj_dict=globals()
	funcs_list=[]
	for item in obj_list:
		if item[:1]!="_":
			func=getattr(m,item)
			funcs_list.append(func)
	return funcs_list

def invoke(windy,request,environ):
	funcs_list=windy.middleware_fuctions
	for func in funcs_list:
		request=func(windy,request,environ)
	return request