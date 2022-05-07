from enum import Enum
import typing as t

import asyncclick as click

from ethbit import web_client

__all__ = (
    "CurrType",
    "get_balances",
    "get_stored_addresses",
)


class CurrType(str, Enum):
    ETH = "eth-"
    BTC = "btc-"


async def exchange_rate(curr: CurrType, vs_curr: str) -> str:
    currency = "ethereum" if curr == CurrType.ETH else "bitcoin"
    params = {"ids": currency, "vs_currencies": vs_curr}
    exchange = (
        await web_client.get(
            "https://api.coingecko.com/api/v3/simple/price", params=params
        )
    ).json()
    return exchange[currency][vs_curr.lower()]


def get_stored_addresses(
    stored_values: dict[str, t.Any] | None, curr_type: CurrType, name: str | None
) -> list[str | None]:
    if not stored_values:
        raise click.UsageError("No addresses provided.")

    stored_addrs = []
    for (key, val) in stored_values.items():
        if key.startswith(curr_type):
            if name and val.get("name") == name:
                stored_addrs.append(val.get("address"))
                break
            else:
                stored_addrs.append(val.get("address"))

    return stored_addrs


def print_dict(title: tuple[str, str], values: dict[str, t.Any]) -> None:
    k, v = title
    click.echo("{:>25} {:>30}".format(k, v))

    for (key, val) in values.items():
        click.echo("{:>10} {:>10}".format(key, val))


async def get_balances(
    stored_values: dict[str, t.Any] | None,
    addresses: list[str],
    vs_curr: str | None,
    get_balance: t.Callable,
) -> tuple[dict[str, str | None], str | None]:
    # Gets the conversion currency from the config file
    if not vs_curr:
        if not stored_values:
            vs_curr = "usd"
        else:
            vs_curr = stored_values.get("eth", {}).get("vs_curr", "usd").lower()

    # Checks if the addresses are valid and get their balances
    balances = await get_balance(addresses, vs_curr)
    return (balances, vs_curr)
