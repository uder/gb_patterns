from pprint import pprint
from windy.templates import render
class TemplateView():
    template = "base.html"

    def __init__(self):
        self.context={}
        self.code='200 OK'

    def get_context(self):
        return {}

    def __call__(self,windy,request):
        self.context=self.get_context(request)
        # self.context.update(request)
        # request=self.context
        code=self.code
        text = render(self.template, **self.context)
        return code, text

class ListView(TemplateView):
    template = "list.html"
    def __init__(self):
        # self.context=self.get_context(request)
        self.code='200 OK'

class CreateView(TemplateView):
    template = "create.html"
    def __init__(self):
        # self.context=self.get_context(request)
        self.code='200 OK'

