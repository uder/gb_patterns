from time import time
from windy.models.logger import WindyLogger
from inspect import isclass,isfunction

def debug(func):
    logger=WindyLogger()
    def wrapper(*args,**kwargs):
        t1=time()
        if isfunction(func):
            result=func(*args,**kwargs)
        elif isclass(func):
            view=func()
            result=view.__call__(*args,**kwargs)
        t2=time()
        logger.log("DEBUG",'debug', f'Name: {func.__name__} Time: {t2-t1}')
        return result
    return wrapper
