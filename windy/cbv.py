from pprint import pprint
from windy.templates import render
from windy.observer import CreateNotifier,Console
class TemplateView():
    template = "base.html"

    def __init__(self):
        self.context={}
        self.code='200 OK'

    def get_context(self,request):
        return {}

    def __call__(self,windy,request):
        self.context=self.get_context(request)
        code=self.code
        text = render(self.template, **self.context)
        return code, text

class ListView(TemplateView):
    template = "list.html"

class CreateView(TemplateView):
    console=Console()
    notifier=CreateNotifier()
    template = "create.html"
    def __init__(self):
        super().__init__()
        self.notifier.attach(self.console)

