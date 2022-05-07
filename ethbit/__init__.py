from web3 import Web3
from httpx import AsyncClient

from ethbit import commands, config, types

__version__ = "0.1.0"
__all__ = ("commands", "config", "w3", "types", "web_client")


web_client = AsyncClient()
w3 = Web3()
