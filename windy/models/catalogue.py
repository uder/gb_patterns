import abc

class Catalogue(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def list_children(self):
        pass

