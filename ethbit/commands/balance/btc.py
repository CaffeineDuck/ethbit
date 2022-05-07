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
    get_stored_addresses,
    get_stored_name_address,
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
    # Gets all the stored addresses
    stored_addrs = get_stored_addresses(ctx, CurrType.BTC)

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
        click.echo(f"{invalid_addrs} (is/are) not valid BTC addresse(s).", err=True)

    # Stop if there are no valid addresses
    if not new_addrs:
        return click.echo("No valid addresses found.", err=True)

    # Print the balances
    print_dict(("Address", f"Balance ({vs_curr.upper()})"), balances)
