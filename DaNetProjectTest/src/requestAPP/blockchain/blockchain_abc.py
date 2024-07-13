from abc import ABC, abstractmethod


class Blockchain:

    @abstractmethod
    async def get_balance(self, address: str):
        pass

    @abstractmethod
    async def get_balance_batch(self, addresses: str):
        pass