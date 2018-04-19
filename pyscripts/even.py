#closures 

a = list(range(100)) #defined list

global stack #global variable
stack = [] #initialize as empty list

def even():
	global stack
	#stack = []

	def app(stack,a): #inner function

		for i in a:
			if i%2==0: stack.append(i)
	return app #function


if __name__ == '__main__':
	b = even()
	print(b) #closure
	print(stack)
	print('after calling {}'.format(b.__name__))
	b(stack,a) #function call
	print(stack)