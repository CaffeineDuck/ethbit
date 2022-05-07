import asyncclick as click

from .balance import kraken_bal

__all__ = ("kraken",)


@click.group("kra", help="Kraken API")
def kraken():
    ...


kraken.add_command(kraken_bal)
