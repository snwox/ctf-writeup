from base64 import b64decode as btoa
s="c2hpZmwK00c2hpZmwK01c2hpZmwK02c2hpZmwK03c2hpZmwK04c2hpZmwK05c2hpZmwK06c2hpZmwK07c2hpZmwK08c2hpZmwK09c2hpZmwK0ac2hpZmwK0bc2hpZmwK0cc2hpZmwK0dc2hpZmwK0ec2hpZmwK0fc2hpZmwK10c2hpZmwK11c2hpZmwK12c2hpZmwK13c2hpZmwK14c2hpZmwK15c2hpZmwK16c2hpZmwK17c2hpZmwK18c2hpZmwK19c2hpZmwK1ac2hpZmwK1bc2hpZmwK1cc2hpZmwK1dc2hpZmwK1ec2hpZmwK1fc2hpZmwK20c2hpZmwK21c2hpZmwK22c2hpZmwK23c2hpZmwK24c2hpZmwK25b3BYT1IK000005b3BYT1IK050005b3BYT1IK000005b3BYT1IK03030Ab3BYT1IK0A030Ab3BYT1IK03030Ab3BfcGwK040db3BfcGwK080db3BfcGwK0c0db3BfcGwK100db3BfcGwK140db3BfcGwK180db3BfcGwK1c0db3BfcGwK200db3BfcGwK240db3BYT1IK141422b3BYT1IK221422b3BYT1IK141422b3BYT1IK252511b3BYT1IK112511b3BYT1IK252511b3BYT1IK010121b3BYT1IK210121b3BYT1IK010121b3BYT1IK0b0b16b3BYT1IK160b16b3BYT1IK0b0b16b3BfTUkK000db3BfTUkK030db3BfTUkK060db3BfTUkK090db3BfTUkK0c0db3BfTUkK0f0db3BfTUkK120db3BfTUkK150db3BfTUkK180db3BfTUkK1b0db3BfTUkK1e0db3BfTUkK210db3BfTUkK240d"
a={"A":"b3BBTkQK",
 "Z":"b3BfT1IK",
 "d":"b3BYT1IK",
 "G":"b3BfcGwK",
 "m":"b3BfTUkK",
 "l":"b3BESVYK",
 "N":"TU9ET1AK",
 "q":"c2hpZmwK",
 "E":"c2hpZnIK"
}
b=dict()
for k in a:
    b[a[k]]=k

i=0
c=''
ops=[]
args=[]
origin=btoa("w4Vkw4bDqcOxwqbDj8OKw7XDmcOqZHLDinBdw4/Dul9mw4JfbsOIaG7Dil3DmWxfbMOTwr3DkWJoYg==")
flags=list(map(ord,btoa("w4Vkw4bDqcOxwqbDj8OKw7XDmcOqZHLDinBdw4/Dul9mw4JfbsOIaG7Dil3DmWxfbMOTwr3DkWJoYg==").decode('utf-8'))) # don't use ascii

while i<len(s): # parsing app opcodes and arguments
    c+=s[i]
    i+=1
    for data in a.values():
        if c.find(data)!=-1:
            idx=c.find(data)
            if idx!=0:
                # print(c[:idx])
                args.append(c[:idx])
            ops.append(b[c[idx:]])
            # print(b[c[idx:]])
            c=''
            break
args.append('240d')

for i in range(len(args)-1,-1,-1): # decrypt
    op=ops[i]
    match op:  # it requires python version 3.10 <=
        case 'd':
            a=int(args[i][:2],16)
            b=int(args[i][2:4],16)
            c=int(args[i][4:6],16)
            flags[a]=flags[b]^flags[c]
            # print(f"flags[{a}] = flags[{b}]^flags[{c}]")
        case 'G':
            a=int(args[i][:2],16)
            b=int(args[i][2:4],16)
            flags[a]=flags[a]-b&0xff
            # print(f"flags[{a}] = flags[{a}]-{b}")
        case 'm':
            a=int(args[i][:2],16)
            b=int(args[i][2:4],16)
            flags[a]=flags[a]+b&0xff
            # print(f"flags[{a}] = flags[{a}]+{b}")
        case 'q':
            a=int(args[i][:2],16)
            flags[a]>>=1
            # print(f"flags[{a}] = flags[{a}] >> 1")
# for i,j in zip(ops,args):
#     print(f"{i} : {j}")
print(len(flags))
print(''.join(list(map(chr,flags))))
