from web3 import Web3
from httpx import AsyncClient

from ethbit import commands, config

__version__ = "0.1.0"
__all__ = ("commands", "config", "w3", "web_client")


web_client = AsyncClient()
w3 = Web3()
