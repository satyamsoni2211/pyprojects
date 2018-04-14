d = ['i','like','sung','samsung','mobile','ice','cream','man','go','mango']
s = 'ilikesamsung'
def break_str(s):
    flag = False
    s2 = s
    c2 = []
    while flag is False:
        for i in d:
            if s2.startswith(i):
                c2.append(i)
                print c2
                if len(s2) == len(i):
                    flag = True
                else:
                    s2 = s2[len(i):]
            if i in s2:
                if len(i) > 2:
                    c2.append(s2[:s2.index(i)])
                    c2.append(i)
                    if len(s2) == (s2.index(i) + (len(i) - 1)):
                        flag = True
                    else:
                        s2 = s2[s2.index(i) + (len(i) - 1):]


    return c2


str = break_str(s)
print str
#print 'Ye\nthe string can le segmented as \'{}\''.format(' '.join(str))