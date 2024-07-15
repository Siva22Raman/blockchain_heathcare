from flask import Flask, jsonify, request, render_template, redirect, url_for
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'records': block['records'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/records/new', methods=['POST'])
def new_record():
    patient_id = request.form['patient_id']
    patient_name = request.form['patient_name']
    diagnosis = request.form['diagnosis']
    
    index = blockchain.new_record(patient_id, patient_name, diagnosis)
    
    return redirect(url_for('index'))

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return render_template('chain.html', chain=blockchain.chain)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
