import cx_Oracle as cx
d = {}
with open('cred.txt') as fh:
    for i in fh:
        a = i.rstrip('\n').split(':')
        print a
        d[a[0]] = a[1]

#conn_cx = cx.connect('{}/{}'.format(d['user'],d['pass']))
conn_cx = cx.connect('{}/{}'.format('satyam','satyam123'))


curs = conn_cx.cursor()
#curs.callproc('get_emp',['Donald',198])
