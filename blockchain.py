# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 10:25:53 2019
@author: pidwid
to be installed - Flask, Postman
"""
# to give blocks a timestamp
import datetime
# to hash the blocks
import hashlib
# to encode blocks
import json
# jsonify to communicate with postman
from flask import Flask, jsonify

"""Building a blockchain"""


class Blockchain:

    # init function
    def __init__(self):
        # chain in block-chain (a list)
        self.chain = []
        # to create a genesis block (first block)
        self.create_block(proof=1, previous_hash='0')

    # create a new block
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    # get last block of the current chain
    def get_previous_block(self):
        return self.chain[-1]

    # proof of work will be a number that is easy to get(or verify) but hard to find
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # str will make the proof equation a string for hashlib libraray and encode will add b before it for
            # hashlib to accept format, then if proof equation = 5, str will make it '5' and encode will make it
            # b'5' then hexdigest will generate a hexvalue in hexadecimal format.
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # if first four digit of hash_opearation is 0 then minor succeeds otherwise loses
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        # on success return new_proof ( i.e. bitcoin equivalent)
        return new_proof

    def hash(self, block):
        # each block has a dictionary of 4 keys as defined earlier soo now we will use this dictionary and
        # convert it into json string format by the use of dumps function of json library.
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        # to check if out block is valid soo we will check that the prev hash of each block is equal
        # to hash of its prev block and proof of each block is valid according to our proof of work function
        previous_block = chain[0]
        block_index = 1
        # initialise previous_block as first block of the chain and a looping variable for while loop
        while block_index < len(chain):
            block = chain[block_index]
            # check if prev_hash of current block is equal to previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False, 1
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # checl if proof has first 4 zero
            if hash_operation[:4] != ['0000']:
                return False, 2
            previous_block = block
            block_index += 1
            # if everything is good increment block_index and return true
            return True


""" Creating a web app by using flask """
app = Flask(__name__)


""" Creating a blockchain"""
blockchain = Blockchain()


""" Mining a blockchain"""
@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congrats, you just mined a block', 'index': block['index'], 'timestamp': block['timestamp'],
                'proof': block['proof'], 'previous_hash': block['previous_hash']}
    return jsonify(response), 200


""" Getting a full Blockchain"""
@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200


""" Checking if blockchain is valid """
@app.route("/is_valid", methods=["GET"])
def is_valid():
    response = {'validity': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200


"""Running the app"""
app.run(host='0.0.0.0', port=5000)
