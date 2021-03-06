import os
import random
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub

app = Flask(__name__)
CORS(app, resources={ r'/*': { 'origins': 'http://127.0.0.1:3000' } })
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route('/')
def route_default():
    return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/range')
def route_blockchain_rage():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    return jsonify(blockchain.to_json()[::-1][start:end])

@app.route('/blockchain/length')
def route_blockchain_length():
    return jsonify(len(blockchain.chain))

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    trasaction_data = request.get_json()
    transaction = transaction_pool.existing_transation(wallet.address)

    if transaction:
        transaction.update(
            wallet,
            trasaction_data['recipient'],
            trasaction_data['amount']
        )
    else:
        transaction = Transaction(
            wallet,
            trasaction_data['recipient'],
            trasaction_data['amount']
        )

    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({
        'address': wallet.address,
        'balance': wallet.balance
    })

ROOT_PORT = 5000
PORT = ROOT_PORT
if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    r = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    print(f'result: {r.json()}')

    result_blockchain = Blockchain.from_json(r.json())


    try:
        blockchain.replace_chain(result_blockchain)
        print('\n-- Successfully synchronized the local chain')
    except Exception as e:
        print(f'\n-- Error synchronizing: {e}')

if os.environ.get('SEED_DATA') == 'True':
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json(),
            Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json(),
        ])

app.run(port=PORT)