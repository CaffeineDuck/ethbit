import asyncclick as click

from .eth import balance_eth

__all__ = ("balance",)


@click.group("balance", help="Show balance for your addresses")
async def balance():
    ...


balance.add_command(balance_eth)
