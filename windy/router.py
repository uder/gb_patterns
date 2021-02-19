import os, json
from importlib import import_module
from inspect import getmembers,isfunction,isclass
from windy.include_patterns.singleton import Singleton
from pprint import pprint

class Router(metaclass=Singleton):
    routes={}
    not_found=None

    @classmethod
    def add_route(cls, url):
        def inner(view):
            cls.routes.update({url: view})
            return view

        return inner

    def __init__(self):
        self.init_routes()

    def init_routes(self):
        dirname = os.path.dirname(__file__)
        config_file = os.path.join(dirname, "conf/routes.json")
        with open(config_file, "r") as f:
            json_conf = json.load(f)

        for item in json_conf:
            self.routes.update({item['path']:self._get_view_by_name(item['handler'])})

    def get_view(self,route):
        view=self.routes.get(route,self.not_found)
        if isfunction(view):
            result=view
        elif isclass(view):
            result=view()
        return result

    def _get_view_by_name(self,handler):
        view = self.not_found
        m = import_module('windy.views')
        callable_list=getmembers(m,isfunction)
        callable_list.extend(getmembers(m,isclass))
        for name, func in callable_list:
            if name == handler:
                view = func
            elif name == 'not_found':
                self.not_found=func

        return view
