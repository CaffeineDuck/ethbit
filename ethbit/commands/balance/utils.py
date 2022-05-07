from enum import Enum
import typing as t

import asyncclick as click
from asyncclick import Context

from ethbit.types import Addresses
from ethbit import web_client

__all__ = ("get_stored_addresses", "get_stored_name_address", "CurrType")


class CurrType(str, Enum):
    ETH = "eth."
    BTC = "btc."


async def exchange_rate(curr: CurrType, vs_curr: str) -> str:
    currency = "ethereum" if curr == CurrType.ETH else "bitcoin"
    exchange = (
        await web_client.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": currency, "vs_currencies": vs_curr},
        )
    ).json()
    return exchange[currency][vs_curr.lower()]


def get_stored_addresses(ctx: Context, curr_type: CurrType) -> Addresses:
    if not ctx.default_map:
        raise click.UsageError("No addresses provided.")
    return [val for (key, val) in ctx.default_map.items() if key.startswith(curr_type)]


def get_stored_name_address(addresses: Addresses, name: str) -> str | None:
    try:
        named_addr = [
            addr.get("address") for addr in addresses if addr.get("name") == name
        ][0]
    except IndexError:
        raise click.UsageError(f"No address found for name {name}.")

    return named_addr


def print_dict(title: tuple[str, str], values: dict[str, t.Any]) -> None:
    k, v = title
    click.echo("{:>25} {:>30}".format(k, v))

    for (key, val) in values.items():
        click.echo("{:>10} {:>10}".format(key, val))
