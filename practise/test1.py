def count_str(s):
    st,dc = [],[]
    for i in range(len(s)):
        if s[i] == '(':
            st.append((i,s[i]))
        elif s[i] == ')':
            if len(st)!=0:
                dc.append(st.pop())
                dc.append((i, s[i]))
    return dc
s = '()(()))))'
d = dict(count_str(s))
str = ''.join([s[i] for i in sorted(d.keys())])
print 'length of largest matching parameter string {} is {}'.format(str,len(str))

