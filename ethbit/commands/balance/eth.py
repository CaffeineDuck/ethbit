from decimal import Decimal

import asyncclick as click
from asyncclick.core import Context

from ethbit import w3
from ethbit.config import CONTEXT_SETTINGS

from .utils import (
    CurrType,
    exchange_rate,
    get_stored_addresses,
    print_dict,
    get_balances,
)


def check_valid_address(addresses: list[str | None]) -> list[str]:
    return [addr for addr in addresses if w3.isAddress(addr) and addr]


async def get_balance(addresses: list[str], vs_curr: str) -> dict[str, str]:
    balances_wei = {addr: w3.eth.get_balance(addr) for addr in addresses if addr}
    rate = await exchange_rate(CurrType.ETH, vs_curr.lower())
    return {
        # Converting Wei to eth to required currency
        addr: str(w3.fromWei(balance, "ether") * Decimal(rate))
        for (addr, balance) in balances_wei.items()
    }


@click.command(
    "eth", short_help="Balance of ETH addresses.", context_settings=CONTEXT_SETTINGS
)
@click.argument("addresses", nargs=-1, type=str, required=False)
@click.option("--name", "-n", type=str, help="Name of the address.", required=False)
@click.option("--vs-curr", "-c", type=str, help="Currency to convert to.")
@click.pass_context
async def balance_eth(
    ctx: Context,
    addresses: list[str | None] | None,
    name: str | None,
    vs_curr: str | None,
) -> None:
    """
    Balance of ETH addresses.
    """
    if name and addresses:
        raise click.BadArgumentUsage("You can't use both --name and addresses.")

    if not addresses:
        addresses = get_stored_addresses(ctx.default_map, CurrType.ETH, name)

    if not addresses:
        return click.echo("No addresses provided.")

    valid_addrs = check_valid_address(addresses)

    balances, curr = await get_balances(
        ctx.default_map, valid_addrs, vs_curr, get_balance
    )

    # Print the balances
    currency = curr or "USD"
    print_dict(("Address", f"Balance ({currency.upper()})"), balances)
