from decimal import Decimal
import hashlib
import base58
import binascii
import asyncio

import asyncclick as click
from asyncclick.core import Context

from ethbit import web_client
from ethbit.config import CONTEXT_SETTINGS

from .utils import (
    CurrType,
    exchange_rate,
    get_balances,
    get_stored_addresses,
    print_dict,
)


def check_valid_address(addresses: list[str | None]) -> list[str]:
    # Check if a bitcoin address is valid
    def check_validity(address: str) -> bool:
        base58Decoder = base58.b58decode(address).hex()
        prefixAndHash = base58Decoder[:-8]
        checksum = base58Decoder[-8:]
        hash_ = prefixAndHash
        for _ in range(1, 3):
            hash_ = hashlib.sha256(binascii.unhexlify(hash_)).hexdigest()
        return checksum == hash_[:8]

    # Return all the valid addresses
    return [addr for addr in addresses if addr and check_validity(addr)]


async def get_balance_individual_address(address: str) -> Decimal:
    exchange = (
        await web_client.get(
            "https://blockchain.coinmarketcap.com/api/address",
            params={"address": address},
        )
    ).json()
    return Decimal(exchange.get("balance"))


async def get_balance(addresses: list[str], vs_curr: str) -> dict[str, str]:
    tasks = [get_balance_individual_address(addr) for addr in addresses]
    balances = await asyncio.gather(*tasks)
    addr_bal_map = zip(addresses, balances)
    rate = await exchange_rate(CurrType.BTC, vs_curr.lower())

    return {
        # Converting Wei to eth to required currency
        addr: str(balance * Decimal(rate))
        for (addr, balance) in addr_bal_map
    }


@click.command(
    "btc", short_help="Balance of BTC addresses.", context_settings=CONTEXT_SETTINGS
)
@click.argument("addresses", nargs=-1, type=str, required=False)
@click.option("--name", "-n", type=str, help="Name of the address.", required=False)
@click.option("--vs-curr", "-c", type=str, help="Currency to convert to.")
@click.pass_context
async def balance_btc(
    ctx: Context,
    addresses: list[str | None] | None,
    name: str | None,
    vs_curr: str | None,
) -> None:
    """
    Balance of BTC addresses.
    """
    if name and addresses:
        raise click.BadArgumentUsage("You can't use both --name and addresses.")

    if not addresses:
        addresses = get_stored_addresses(ctx.default_map, CurrType.BTC, name)

    if not addresses:
        return click.echo("No addresses provided.")

    valid_addrs = check_valid_address(addresses)
    stored_curr = (
        ctx.default_map.get("main", {}).get("default_currency")
        if ctx.default_map
        else None
    )

    balances, curr = await get_balances(
        stored_curr,
        valid_addrs,
        vs_curr,
        get_balance,
    )

    # Print the balances
    currency = curr or "USD"
    print_dict(("Address", f"Balance ({currency.upper()})"), balances)
