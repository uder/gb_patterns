import os
import json
from windy.include_patterns.singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self,confdir=""):
        try:
            self.confdir
        except:
            self.confdir=confdir

        self.logconfig=self.get_log_config()

    def get_log_config(self):
        logconfig=os.path.join(self.confdir,'log.json')
        # conf_dict={}
        with open (logconfig,'r') as f:
            conf_dict=json.load(f)

        return conf_dict