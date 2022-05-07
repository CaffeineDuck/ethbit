import asyncclick as click

from .eth import balance_eth
from .btc import balance_btc

__all__ = ("balance",)


@click.group("bal", help="Show balance for your addresses")
async def balance():
    ...


balance.add_command(balance_eth)
balance.add_command(balance_btc)
