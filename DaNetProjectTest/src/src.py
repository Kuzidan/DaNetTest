from fastapi import FastAPI

from .requestAPP.request_app import RequestAPP
from .requestAPP.blockchain.modules.ethereum_polygon import EthereumPolygon


app = FastAPI()
blockchain = RequestAPP(EthereumPolygon())


@app.get('/get_balance/{address}')
async def get_balance(address: str):
    balance = await blockchain.get_balance(address)
    return {'address': address, 'balance': balance}

@app.get('/get_balance_batch/{addresses}')
async def get_balance_batch(addresses: str):
    balances = await blockchain.get_balance_batch(addresses)
    return balances