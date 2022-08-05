from flask import Flask, jsonify, request
from uuid import uuid4

from hadcoin import Blockchain

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route("/mine_block", methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)

    previous_hash = blockchain.get_hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver='Fernando', amount=1)

    new_block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Parabens, voce minerou um bloco!',
        'index': new_block['index'],
        'timestamp': new_block['timestamp'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash'],
        'transaction': new_block['transactions']
    }
    return jsonify(response), 200


@app.route("/get_chain", methods=['GET'])
def get_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200


@app.route("/is_valid", methods=['GET'])
def is_valid():
    return jsonify({
        'is_valid': blockchain.is_chain_valid(blockchain.chain)
    }), 200


@app.route("/add_transaction", methods=['POST'])
def add_transaction():
    json = request.get_json()
    transactions_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transactions_keys):
        return 'Alguns elementos estão faltando', 400
    index = blockchain.add_transaction(
        json['sender'],
        json['receiver'],
        json['amount']
    )
    response = {
        'message': f'Esta transação será adicionada ao bloco {index}'
    }
    return jsonify(response), 201


@app.route("/connect_node", methods=['POST'])
def connect_node():
    data = request.json
    nodes = data.get('nodes')
    if nodes is None:
        return "Vazio", 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        'message': 'Todos os nós conectados.',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route("/replace_chain", methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            'message': 'Chain substituída',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Não ouve substituição',
            'current_chain': blockchain.chain
        }
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5001)
