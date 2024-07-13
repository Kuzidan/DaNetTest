import asyncio

from web3 import Web3
from aiohttp import ClientSession
from typing import List

from src.requestAPP.blockchain.settings import _POLYGON_RPC_URL, _POLYSCAN_BASE_URL, _POLYSCAN_API_KEY
from src.requestAPP.blockchain.blockchain_abc import Blockchain


class EthereumPolygon(Blockchain):

    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(_POLYGON_RPC_URL))
        self.base_url = _POLYSCAN_BASE_URL
        self.api_key = _POLYSCAN_API_KEY
        self.session = ClientSession()


    async def __make_polygonscan_api_request(self, module: str,
                                             action: str,
                                             params: List[str],
                                             session: ClientSession):
        url = f"{self.base_url}?module={module}&action={action}&{'&'.join(params)}&apikey={self.api_key}"
        result = await session.get(url)

        if result.status == 200:
            return await result.json()

        return {"Something Wrong!": None}

    async def get_balance(self, address: str):
        module = 'account'
        action = 'balance'
        params = [f'address={address}', 'tag=latest']
        response = await self.__make_polygonscan_api_request(module, action, params, self.session)
        if response:
            balance_in_wei = int(response['result'])
            balance_in_matic = self.web3.from_wei(balance_in_wei, 'ether')
            return balance_in_matic
        else:
            return None

    async def get_balance_batch(self, addresses: str):
        address_list: List[str] = addresses.split(',')
        module: str = 'account'
        action: str = 'balance'
        params: List[List] = [[f'address={address}', 'tag=latest'] for address in address_list]
        tasks: List[asyncio.Task] = [asyncio.create_task(self.__make_polygonscan_api_request(module, action, parameters, self.session)) for parameters in params]
        results = await asyncio.gather(*tasks)
        response_result = [
            {'address': address, 'balance': self.web3.from_wei(int(response['result']), 'ether')}
            for address, response in zip(address_list, results) if 'result' in response
        ]
        return response_result

