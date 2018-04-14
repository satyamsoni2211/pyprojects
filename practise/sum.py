a = [1,2,3,4]

# function to use getattr
mode = 'append'

def func(*args,**kwargs):
     print kwargs
     out = getattr(a,kwargs['b'])
     if kwargs['b'] == 'pop':
        return out()
     else:
         return out(kwargs['data'])

func(1,2,b='pop',data=1)
print a

def product(*args, **kwargs):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * kwargs['repeat']
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)

for i in permutations('abc',r=2):
    print i