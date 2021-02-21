import abc
from datetime import datetime

class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject=None
        self._observer_state=None

    def set_subject(self,publisher):
        self._subject=publisher

    @abc.abstractmethod
    def update(self, arg):
        pass

class Publisher():
    def __init__(self):
        self._observers=set()
        self._publisher_state=None

    def attach(self,observer):
        observer.set_subject(self)
        self._observers.add(observer)

    def detach(self,observer):
        observer.set_subject(None)
        self._observers.discard(observer)

    def _notify(self):
        for obs in self._observers:
            obs.update(self._publisher_state)

class Console(Observer):
    delimiter="---"
    def update(self, arg):
        print(self.delimiter)
        print(f'{datetime.now().isoformat(" ","seconds")}: {arg}')
        print(self.delimiter)


class CreateNotifier(Publisher):
    @property
    def text(self):
        return self._publisher_state

    @text.setter
    def text(self,text):
        self._publisher_state=text
        self._notify()