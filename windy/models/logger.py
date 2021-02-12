import os
from datetime import datetime
from windy.include_patterns.singleton import Singleton

class WindyLogger(metaclass=Singleton):
    def __init__(self,dir='logs'):
        self.delimiter="---"
        self.eol="\n"
        self.dir=dir

    def log(self,severity,target="messages",message=""):
        date=datetime.now()
        record=f'{date} {severity}: {message}'
        self.log_to_file(target,record)
        self.log_to_console(record)

    def log_to_file(self,target,record):
        filename=target+'.log'
        path=os.path.join(self.dir, filename)
        with open(path,'a') as f:
            f.write(record+self.eol)

    def log_to_console(self,record):
        print(self.delimiter)
        print(record)
        print(self.delimiter)