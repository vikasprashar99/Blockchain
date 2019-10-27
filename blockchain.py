# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 10:25:53 2019
@author: lucky
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


# Building a blockchain
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
            'timestamp': datetime.datetime.now(),
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
            # b'5' then hexdigest will generate a hexvalue
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # if first four digit of hash_opearation is 0 then minor succeeds otherwise loses
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        # on success return new_proof ( i.e. bitcoin equivalent)
        return new_proof



# Mining a blockchain


