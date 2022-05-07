import asyncclick as click

from ethbit.commands.balance import balance
from ethbit.commands.transactions import txn
from ethbit.commands.kraken import kraken
from ethbit.utils import catch_exception

from .commands.setup import add, setup


@click.group()
@catch_exception
def cli():
    ...


# Add all the command groups
cli.add_command(setup)
cli.add_command(balance)
cli.add_command(txn)
cli.add_command(kraken)
cli.add_command(add)

# Start the CLI
cli(_anyio_backend="asyncio")
