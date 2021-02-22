import abc
import os
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

class Email(Observer):
    delimiter="---"
    def update(self, arg):
        print(self.delimiter)
        print(f'{datetime.now().isoformat(" ","seconds")}: Email - {arg}')
        print(self.delimiter)

class Sms(Observer):
    delimiter="---"
    def update(self, arg):
        print(self.delimiter)
        print(f'{datetime.now().isoformat(" ","seconds")}: Sms - {arg}')
        print(self.delimiter)

class LogFile(Observer):
    def __init__(self,logfile):
        super().__init__()
        self.eol="\n"
        self._logfile=self._set_logfile(logfile)

    def _set_logfile(self,string):
        if not string.endswith('.log'):
            string=f'{string}.log'
        logdir='logs'
        return os.path.join(logdir, string)

    def update(self, arg):
        record=f'{datetime.now().isoformat(" ","seconds")}: {arg}{self.eol}'
        with open(self._logfile,"a") as f:
            f.write(record)

class CreateNotifier(Publisher):
    @property
    def arg(self):
        return self._publisher_state

    @arg.setter
    def arg(self,argument):
        self._publisher_state=argument
        self._notify()

