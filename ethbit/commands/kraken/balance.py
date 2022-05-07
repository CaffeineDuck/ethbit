import asyncclick as click
from rich import print
from asyncclick.core import Context
from .utils import call_kraken

from ethbit.config import CONTEXT_SETTINGS

__all__ = ("kraken_bal",)


@click.command(
    "bal", short_help="Balances the current account", context_settings=CONTEXT_SETTINGS
)
@click.pass_context
async def kraken_bal(ctx: Context):
    """Balances the current account"""
    if not ctx.default_map:
        raise click.ClickException(
            "Kraken API key not found, please use 'ethbit setup'"
        )

    main = ctx.default_map.get("main", {})
    api_key = main.get("kraken_api_key")
    api_secret = main.get("kraken_api_sec")

    resp = await call_kraken("/0/private/Balance", {}, api_key, api_secret)
    balance = resp["result"]

    if not balance:
        raise click.ClickException("No balance found")

    print(f"Balance: {balance}")
