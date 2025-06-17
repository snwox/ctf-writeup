from flask import Flask, render_template, request, session, redirect, url_for, Response
from flask_session import Session
from os import urandom, getenv
from hashlib import sha256
from uuid import uuid4
from eth_sandbox.auth import get_shared_secret
from eth_account import Account
from web3 import Web3
from pathlib import Path
from datetime import timedelta
from eth_utils import keccak
from base64 import b64encode, b64decode
import urllib.parse
import eth_sandbox
import requests
import json

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = urandom(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # Choose your preferred session type (e.g., 'redis', 'filesystem', etc.)
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # Sign the session cookies for security
app.config['SESSION_KEY_PREFIX'] = 'session:'
Session(app)

HTTP_PORT = getenv("HTTP_PORT", "8000")
PUBLIC_URL = getenv("PUBLIC_URL", "127.0.0.1")

code = open("/home/ctf/contracts/Bank.sol").read()
@app.route('/')
def index():
    if 'node' in session:
        return render_template("index.html", node=session['node'], code=code)
    else:
        ticket = urandom(8).hex()
        session['ticket'] = ticket
        return render_template("intro.html", ticket=ticket)

@app.route('/launch', methods=['POST'])
def launch():
    if 'node' in session:
        return render_template("index.html", node=session['node'])
    else:
        data = request.get_json()
        if not data or 'answer' not in data:
            return render_template("intro.html", ticket=session.get('ticket'), error="missing answer")
        
        answer = str(data['answer'])
        ticket = session.get('ticket')
        print(answer,ticket)
        if not ticket:
            return Response("invalid ticket", status=400)
        
        uuid = get_uuid(answer, ticket)
        if not uuid:
            return Response("invalid answer", status=400)
        secret = get_shared_secret()
        res = requests.post(f"http://127.0.0.1:{HTTP_PORT}/new", headers={"Authorization":f"Bearer {secret}"}, json={"uuid": uuid})
        node_info = res.json()
        setup_node(node_info)

        return Response("success", status=200) 

@app.route('/mix', methods=['GET'])
def mix():
    if 'node' not in session:
        return redirect(url_for('index'))
    
    abi = json.loads(Path("/home/ctf/compiled/Bank.sol/Bank.json").read_text())["abi"]
    web3 = Web3(Web3.HTTPProvider(session['node']['rpc'],
            request_kwargs={
                "headers": {
                    "Authorization": f"Bearer {get_shared_secret()}",
                    "Content-Type": "application/json",
                },
            },
        ))
    amount = urllib.parse.quote(request.args.get('amount'))
    receiver = urllib.parse.quote(request.args.get('receiver'))
    fee = urllib.parse.quote(request.args.get('fee'))
    code = urllib.parse.quote(request.args.get('code'))

    bank = web3.eth.contract(address=session['node']['bank'], abi=abi)
    address = Account.from_key(session['node']['pvKey']).address
    balance = bank.functions.balance(address).call() / 10**18

    return render_template("result.html", node=session['node'], balance=balance, amount=amount, receiver=receiver, fee=fee, code=code)

@app.route('/vip', methods=['GET'])
def vip():
    if 'node' not in session:
        return redirect(url_for('index'))
    
    address = Account.from_key(session['node']['pvKey']).address
    web3 = Web3(Web3.HTTPProvider(session['node']['rpc'],
            request_kwargs={
                "headers": {
                    "Authorization": f"Bearer {get_shared_secret()}",
                    "Content-Type": "application/json",
                },
            },
        ))
    
    abi = json.loads(Path("/home/ctf/compiled/Bank.sol/Bank.json").read_text())["abi"]
    bank = web3.eth.contract(address=session['node']['bank'], abi=abi)
    balance = bank.functions.balance(address).call() / 10**18
    print(f"vip balance: {balance}")
    is_vip = balance >= 100
    flag = open("/home/ctf/flag").read() if is_vip else "You are not a VIP"
    return render_template("vip.html", balance=balance, is_vip=is_vip, flag=flag)

@app.route('/download', methods=['GET'])
def download():
    if 'node' not in session:
        return redirect(url_for('index'))
    print(request.args)
    amount = request.args.get('amount').encode()
    receiver = request.args.get('receiver').encode()
    fee = request.args.get('fee').encode()
    code = b64decode(request.args.get('code'))
    deployer_pv_key = session['node']['deployer_pv_key'] 
    signed = Account._sign_hash(keccak(receiver+amount+fee+code), deployer_pv_key)
    template = """We assure you that your funds will be safely transfer to the recipient.
To prove, I can even sign your arguments with Account._sign_hash in eth_account module in python!
It will be processed within 12 hours. IF NOT, please DM to admin with the sign below.
scattered addresses -> {} ({} ETH - {}%) (decoded code: {})

Account._sign_hash(keccak(receiver|amount|fee|decoded code), owner_private_key) ( | is concatenation, not the letter itself )
-> {}
    """.format(receiver.decode('latin-1'), amount.decode('latin-1'), fee.decode('latin-1'), code.decode('latin-1'), signed)
    
    resp = Response(template, mimetype="text/plain")
    resp.headers["Content-Disposition"] = "attachment; filename=receipt.txt"
    return resp

def get_uuid(answer, ticket):
    if sha256((ticket + answer).encode()).hexdigest().startswith("0000"):
        return str(uuid4())
    else:
        return None

def setup_node(info):
    info['rpc'] = f"http://{PUBLIC_URL}:{HTTP_PORT}/{info['uuid']}"
    info['pvKey'] = Account.from_mnemonic(info['mnemonic'], account_path=f"m/44'/60'/0'/0/1").key.hex()
    deployer_pv_key = Account.from_mnemonic(info['mnemonic'], account_path=f"m/44'/60'/0'/0/0").key.hex()
    web3 = Web3(Web3.HTTPProvider(info['rpc'],
            request_kwargs={
                "headers": {
                    "Authorization": f"Bearer {get_shared_secret()}",
                    "Content-Type": "application/json",
                },
            },
        ))
    
    deployer = Account.from_key(deployer_pv_key)
    rcpt = eth_sandbox.sendTransaction(web3, {
        "from": deployer.address,
        "data": json.loads(Path("/home/ctf/compiled/Bank.sol/Bank.json").read_text())["bytecode"]["object"],
    })
    bank_address = rcpt.contractAddress

    rpc = info['rpc']
    r = requests.post(rpc, headers={"Authorization": f"Bearer {get_shared_secret()}"}, json={"jsonrpc":"2.0","method":"anvil_setBalance","params":[deployer.address, str(101 * 10 ** 18)],"id":1})
    rcpt = eth_sandbox.sendTransaction(web3, {
        "from": deployer.address,
        "to": bank_address,
        "value": 100 * 10 ** 18,
    })
    info['bank'] = bank_address
    info['deployer'] = deployer.address
    info['deployer_pv_key'] = deployer_pv_key
    info.pop('mnemonic')
    session['node'] = info

if __name__ == '__main__':
    app.run(host="0.0.0.0")