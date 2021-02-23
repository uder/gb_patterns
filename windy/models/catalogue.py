import abc
from windy.include_patterns.mark_mixin import MarkMixin

class Catalogue(MarkMixin, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list_children(self):
        pass

