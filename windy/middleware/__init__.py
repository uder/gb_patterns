import os
import sys
import pkgutil
from importlib import import_module
from inspect import getmembers, isfunction
from pprint import pprint


def iter_namespace(pkg,path):
	return pkgutil.iter_modules(path,pkg.__name__+".")


def import_functions():
	path=os.path.dirname(__file__)
	funcs_list=[]
	for item in iter_namespace(sys.modules[__name__], [path]):
		m = import_module(item.name)
		funcs=_get_funcs(m)
		funcs_list.extend(funcs)
	return funcs_list
			
def _get_funcs(m):
	funcs_list=[]
	for name, func in getmembers(m,isfunction):
		if not name.startswith("_") and sys.modules[__name__].__name__ in func.__module__:
			funcs_list.append(func)
	return funcs_list

def invoke(windy,request,environ):
	funcs_list=windy.middleware_fuctions
	for func in funcs_list:
		request=func(windy,request,environ)
	return request