# l = [5,6]
# b = [3,4]

l,b = [],[]
for i in range(2): l.append(int(raw_input('enter length')))
for i in range(2): b.append(int(raw_input('enter bredth')))
l = [i for i in range(l[0],l[1]+1)]
l = [i for i in range(b[0],b[1]+1)]
sizes = [(i,j) for i in l for j in b]
print sizes
count = 0


def breakCad(dim):
    stack = []
    def breakPieces(dim,stack):
        l,b = dim
        if l > b:
            stack.append((b,b))
            #print '{}X{}'.format(b,b)
            breakPieces((l-b,b),stack)
        elif b>l:
            stack.append((l,l))
            # print '{}X{}'.format(l,l)
            breakPieces((l,b-l),stack)
        elif b == l:
            stack.append((l,b))
            # print '{}X{}'.format(l,b)
            return True
    breakPieces(dim,stack)
    return len(stack)

count = reduce(lambda x,y: x+y,[breakCad(i) for i in sizes])
print 'These cadbusries can be given to {} students'.format(count)
