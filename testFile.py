d={}

d[1] = 'hello'
d[2] = 'stupid'
d[3] = 'cunt'

print(d.keys())
for i in d.keys():
    d[i] = str(i)
print(d)