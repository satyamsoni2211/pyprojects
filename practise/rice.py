
n = 8
price = [1, 5, 8, 9, 10, 17, 17, 20]
prices = dict(zip(range(1,len(price)+1),price))
print prices
def getComb(n):
    return [[i]*(n/i) if n%i==0 else [i,n-i] for i in range(1,n+1)]
print getComb(n)
#
def getmaxPrice(prices,comb):
    price = 0
    for i in comb:
        print sum([int(prices[j]) for j in i])
        count = sum([int(prices[j]) for j in i])
        if count > price: price = count
    return price

print 'max price is {}'.format(getmaxPrice(prices,getComb(len(price))))
