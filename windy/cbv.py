from pprint import pprint
from windy.templates import render
from windy.observer import CreateNotifier,Console,LogFile
from windy.include_patterns.identity_map import IdentityMap

class TemplateView():
    template = "base.html"

    def __init__(self):
        self.context={}
        self.code='200 OK'
        self._publisher=self._init_publisher()
        self._identitymap=IdentityMap()

    def get_context(self,request):
        return {}

    def _init_publisher(self):
        pass

    def _init_notifier_catalogue(self):
        return []

    def notify(self,argument):
        self._publisher.arg = argument

    def __call__(self,windy,request):
        self.context=self.get_context(request)
        code=self.code
        text = render(self.template, **self.context)
        return code, text

class ListView(TemplateView):
    template = "list.html"

class CreateView(TemplateView):
    template = "create.html"
    # def __init__(self):
    #     super().__init__()

    def _init_publisher(self):
        console = Console()
        logfile=LogFile('learning')
        publisher = CreateNotifier()
        publisher.attach(console)
        publisher.attach(logfile)

        return publisher

