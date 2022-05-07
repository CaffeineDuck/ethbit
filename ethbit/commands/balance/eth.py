from decimal import Decimal

import asyncclick as click
from asyncclick.core import Context

from ethbit import w3
from ethbit.config import CONTEXT_SETTINGS

from .utils import CurrType, get_stored_addresses, get_stored_name_address, print_dict


def check_valid_address(addresses: list[str | None]) -> list[str]:
    return [addr for addr in addresses if w3.isAddress(addr) and addr]


def get_balance(addresses: list[str]) -> dict[str, int | Decimal]:
    balances_wei = {addr: w3.eth.get_balance(addr) for addr in addresses if addr}
    return {
        addr: w3.fromWei(balance, "ether") for (addr, balance) in balances_wei.items()
    }


@click.command(
    "eth", short_help="Balance of ETH addresses.", context_settings=CONTEXT_SETTINGS
)
@click.argument("addresses", nargs=-1, type=str, required=False)
@click.option("--name", "-n", type=str, help="Name of the address.", required=False)
@click.pass_context
async def balance_eth(
    ctx: Context, addresses: list[str | None] | None, name: str | None
) -> None:
    """
    Balance of ETH addresses.
    """
    stored_addrs = get_stored_addresses(ctx, CurrType.ETH)

    addresses = (
        [addr.get("address") for addr in stored_addrs]
        if not addresses
        else [get_stored_name_address(stored_addrs, name)]
        if not addresses and name
        else addresses
    )

    new_addrs = check_valid_address(addresses)
    balances = get_balance(new_addrs)

    if new_addrs != list(addresses):
        invalid_addrs = ", ".join(
            [addr for addr in addresses if addr not in new_addrs and addr]
        )
        return click.echo(
            f"{invalid_addrs} (is/are) not valid ETH addresse(s).", err=True
        )

    if not new_addrs:
        return click.echo("No valid addresses found.", err=True)

    print_dict(("Address", "Balance"), balances)
