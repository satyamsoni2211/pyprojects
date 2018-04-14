from functools import wraps

def outer(func):
    import logging
    logging.basicConfig(filename='{}.log'.format(func.__name__), level=logging.INFO)
    logging.info("wrapper before the original function %s" % func.__name__)

    @wraps(func)
    def inner(*args,**kwds):
        logging.info("function {} ran with args:{} and kwargs: {}".format(func.__name__,args,kwds))
        print "running outer\n"
        return func(*args,**kwds)
    return inner

def tme_wrap(func):
    import time
    t1 = time.time()
    @wraps(func)
    def wrapper(*args,**kwargs):
        result = func(*args,**kwargs)
        return result
    t2 = time.time()
    print("function {} completed in {} time".format(func.__name__,t2-t1))
    return wrapper

@outer
@tme_wrap
def func(name,age):
    print "I am %s and my age is %s\n" % (name,age)
func('satyam',21)

#@outer
#def f():
#    print "this function works without arguments \n"
#f()s