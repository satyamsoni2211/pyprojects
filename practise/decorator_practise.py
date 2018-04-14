import os
def dec(prefix):
        def out(func):
            print "Wrapper above function {}".format(func.__name__)
            def wrapper(*args, **kwargs):
                print "{}.checking for the file in directory {}".format(prefix, os.getcwd())
                return func(*args, **kwargs)
            return wrapper
        return out

@dec('Testing')
def chk(file):
    if os.path.exists(file):
        print "File exists"
chk('func.log')