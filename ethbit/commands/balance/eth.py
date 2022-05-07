from decimal import Decimal

import asyncclick as click
from asyncclick.core import Context

from ethbit import w3
from ethbit.config import CONTEXT_SETTINGS

from .utils import (
    CurrType,
    exchange_rate,
    get_stored_addresses,
    get_stored_name_address,
    print_dict,
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
    # Gets all the stored addresses
    stored_addrs = get_stored_addresses(ctx, CurrType.ETH)

    # Gets the conversion currency from the config file
    if not vs_curr:
        vs_curr = (
            ctx.default_map.get("main", {}).get("currency", "USD")
            if ctx.default_map
            else "USD"
        )

    # Convert to lower case
    vs_curr = vs_curr.lower() if vs_curr else "USD"

    # If addresses are not provided read from config file
    if not addresses:
        addresses = (
            [addr.get("address") for addr in stored_addrs]
            if not name
            else [get_stored_name_address(stored_addrs, name)]
        )

    # Checks if the addresses are valid and get their balances
    new_addrs = check_valid_address(addresses)
    balances = await get_balance(new_addrs, vs_curr)  # type: ignore

    # Throw warning for invalid addresses
    if new_addrs != list(addresses):
        invalid_addrs = ", ".join(
            [addr for addr in addresses if addr not in new_addrs and addr]
        )
        click.echo(f"{invalid_addrs} (is/are) not valid ETH addresse(s).", err=True)

    # Stop if there are no valid addresses
    if not new_addrs:
        return click.echo("No valid addresses found.", err=True)

    # Print the balances
    print_dict(("Address", f"Balance ({vs_curr.upper()})"), balances)
