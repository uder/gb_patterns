from time import time
from windy.models.logger import WindyLogger

def debug(func):
    logger=WindyLogger()
    def wrapper(*args,**kwargs):
        t1=time()
        result=func(*args,**kwargs)
        t2=time()
        logger.log("DEBUG",'debug', f'Name: {func.__name__} Time: {t2-t1}')
        return result
    return wrapper
