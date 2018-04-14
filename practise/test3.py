n = 10000

#this program is for prime number
def prime(n):
    cnt,pr=0,[]#2 is not prime
    for i in xrange(3,n+1):
        if len([j for j in range(2,i) if i%j == 0]) == 0:
            pr.append(i)
            cnt += 1
    return ((i,j) for i,j in zip(pr[:n],pr[1:]) if j-i == 2)
print len(list(prime(n)))

#this would print the output
