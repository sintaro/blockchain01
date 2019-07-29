#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import json
import logging
import sys
import time

import utils

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
MINING_DIFICULTY = 3
MINING_SENDER = 'THE BLOCKCHAIN'
MINING_REWORD = 1.5

class BlockChain(object):
	def __init__(self,blocakchain_address=None):
		self.transaction_pool = []
		self.chain = []
		self.create_block(0, self.hash({}))
		self.blocakchain_address = blocakchain_address

	def create_block(self, nonce, previous_hash):
		block = utils.sorted_dict_by_key({
			'timestamp': time.time(),
			'transactions': self.transaction_pool,
			'nonce':nonce,
			'previous_hash':previous_hash
		})
		self.chain.append(block)
		self.transaction_pool = []
		return block

	def hash(self, block):
		sorted_block = json.dumps(block,sort_keys=True)
		return hashlib.sha256(sorted_block.encode()).hexdigest()

	def add_transaction(self, sender_blockchain_address,
						recipient_blockchain_address, value):
		transaction = utils.sorted_dict_by_key({
			'sender_blockchain_address':sender_blockchain_address,
			'recipient_blockchain_address':recipient_blockchain_address,
			'value':float(value)
		})
		self.transaction_pool.append(transaction)
		return True

	def valid_proof(self, transactions, previous_hash, nonce,
					difficulty=MINING_DIFICULTY):
		guess_block = utils.sorted_dict_by_key({
			'transactions': transactions,
			'nonce':nonce,
			'previous_hash':previous_hash
		})
		guess_hash = self.hash(guess_block)
		return guess_hash[:difficulty] == '0'*difficulty

	def proof_of_work(self):
		transactions = self.transaction_pool.copy()
		previous_hash = self.hash(self.chain[-1])
		nonce = 0
		while self.valid_proof(transactions, previous_hash,nonce) is False:
			nonce +=1
		return nonce

	def mining(self):
		self.add_transaction(
			sender_blockchain_address=MINING_SENDER,
			recipient_blockchain_address=self.blocakchain_address,
			value=MINING_REWORD)
		nonce = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1])
		self.create_block(nonce,previous_hash)
		logger.info({'action':'mining','status':'success'})
		return True

if __name__== '__main__':
	my_blockchain_address = 'my_blockchain_addres'
	block_chain = BlockChain(blocakchain_address=my_blockchain_address)

	block_chain.add_transaction('A','B',1.0)
	block_chain.mining()
	utils.pprint(block_chain.chain)

	block_chain.add_transaction('C','D',3.0)
	block_chain.add_transaction('D','B',2.0)
	block_chain.mining()
	utils.pprint(block_chain.chain)
