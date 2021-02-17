from windy.templates import render
class TemplateView():
    def __init__(self):
        self.template="base.html"

    def __call__(self,request):
        text = render(self.template, **request)
        return code, text

class ListView(TemplateView):
    def __init__(self,):
        self.template="list.html"

    def get_context(self):
        return