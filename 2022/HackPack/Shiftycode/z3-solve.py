from z3 import *

s=Solver()
ar=[Int('a_%d'%i) for i in range(27)]
for i in range(len(ar)):
    s.add(eval(f'ar[{i}]>=32,ar[{i}]<=127'))
s.add(ar[0]==ord('f'),
ar[1]==108,
ar[2]==97,
ar[4]==123,
ar[26]==125,
ar[3]==103)
s.add(ar[14]==ar[19],
ar[5]+ar[7]==204,
ar[7]+ar[6]==216,
204+ar[6]-100==225,
ar[9]+11==ar[8],
ar[10]+66==ar[8],
ar[12]+ar[11]-ar[8]==103,
ar[12]+ar[10]-ar[9]==ar[11]-41,
ar[11]-ar[10]==53,
ar[14]==ar[19],
ar[15]==ar[18],
ar[16]==ar[7],
ar[13]-ar[18]-ar[17]==0,
ar[13]-54==ar[14],
ar[19]*2==ar[23],
ar[20]==ar[16],
ar[22]==ar[10],
ar[21]/2-6==ar[22],
ar[16]==ar[7],
ar[13]-ar[18]-ar[17]==0,
ar[17]<ar[18],
ar[17]>=ar[19],
ar[18]-ar[19]==2,
ar[13]-54==ar[14],
ar[19]*2==ar[23],
ar[20]==ar[16],
ar[22]==ar[10],
ar[21]/2-6==ar[22],
ar[25]-ar[24]==5,
ar[25]-ar[21]==11)
print(s.check())
if s.check()==sat:
    m=s.model()
    for i in range(27):
        try:
            print(chr(int(str(m[ar[i]]))),end='')
        except:
            print('x',end='')
            continue
            
