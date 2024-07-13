from .blockchain.blockchain_abc import Blockchain


class RequestAPP:

    def __init__(self, blockchain: Blockchain):
        self._blockchain = blockchain

    def get_balance(self, address: str):
        return self._blockchain.get_balance(address)

    def get_balance_batch(self, addresses: str):
        return self._blockchain.get_balance_batch(addresses)
