import os, json
from importlib import import_module
from inspect import getmembers,isfunction
from pprint import pprint

class Router():
    routes={}
    not_found=None

    @classmethod
    def add_route(cls, url):
        def inner(view):
            cls.routes.update({url: view})
            return view

        return inner

    @classmethod
    def init_routes(cls):
        dirname = os.path.dirname(__file__)
        config_file = os.path.join(dirname, "conf/routes.json")
        with open(config_file, "r") as f:
            json_conf = json.load(f)

        for item in json_conf:
            cls.routes.update({item['path']:cls._get_view_by_name(item['handler'])})

    @classmethod
    def get_view(cls,route):
        view=cls.routes.get(route,cls.not_found)
        return view

    @classmethod
    def _get_view_by_name(cls,handler):
        view = cls.not_found
        m = import_module('windy.handlers')
        for name, func in getmembers(m, isfunction):
            if name == handler:
                view = func
            elif name == 'not_found':
                cls.not_found=func

        return view
