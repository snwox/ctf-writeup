key=0xdc35849333c6a8

out=0x781494ac201977

flag=key^out

d=format(flag,'b')
ar=[
    d[:9],
    d[9:18],
    d[18:21],
    d[21:25],
    d[25:27],
    d[27:30],
    d[30:35],
    d[35:41],
    d[41:48],
    d[48:56]
]

rev=[2,5,8,3,6,9,0,4,7,1]
table={}
for i,j in enumerate(rev):
    table[i]=j
rev_ar=[0]*10
for k in table:
    rev_ar[table[k]]=ar[k]
rev_ar=rev_ar[::-1]
b=format(int(''.join(rev_ar),2),'056b')
f=''
for i in range(0,len(b),7):
    f+=chr(int(b[i:i+7],2))
print(f[::-1])
