
import os
import logging

global loggers
loggers = {}

def dec(func):
		
		def wrapper(*args,**kwargs):
				logger = getlog(func.__name__) #gettng the logger handle 
				logger.info('This is decorator for function {}'.format(func.__name__))
				logger.info('calling function {}'.format(func.__name__)) 
				logger.info('calling function {} with arguments {}'.format(func.__name__,' '.join([str(i) for i in args])))
				return func(*args,**kwargs)
		return wrapper

def getlog(name):
	global loggers
	if name in loggers.keys():
		return loggers[name]
	else:
		logging.basicConfig(level=logging.INFO)
		logger = logging.getLogger(name)
		handler = logging.FileHandler('{}.log'.format(name))
		handler.setLevel(logging.INFO)
		logger.addHandler(handler)
		loggers[name] = logger
		return logger

@dec
def identity(a):
	print('id for var {} is {}'.format(a,id(a)))

@dec
def sums(a):
	b = 1
	return a+b


b = 'satyam'
a = 2

print(identity.__name__)
identity(b)
print('calling sums')
print(sums(a))