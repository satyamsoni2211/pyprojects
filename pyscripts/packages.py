import subprocess as s
p = s.Popen('pip freeze',stdout=s.PIPE,shell=True)
out,err = p.communicate()
packages = [i.split('==')[0] for i in out.decode().strip('\r\n').split('\r\n')]
print(packages)
print('upgrading packages')
print ('pip install --upgrade {}'.format(' '.join(packages)))
s.call('pip install --upgrade {}'.format(' '.join(packages)))
print('done')