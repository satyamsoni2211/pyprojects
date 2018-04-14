def recip(s):
    a = [chr(i) for i in range(65, 91)]
    print ''.join([a[len(a)-len(a[:a.index(i)+1])] for i in s])
recip('PRAKHAR')
recip('VARUN')




