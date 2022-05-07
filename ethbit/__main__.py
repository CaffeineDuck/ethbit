import asyncclick as click

from ethbit.commands.balance import balance
from ethbit.commands.transactions import txn

from .commands.setup import setup


@click.group()
def cli():
    ...


if __name__ == "__main__":
    # Add all the command groups
    cli.add_command(setup)
    cli.add_command(balance)
    cli.add_command(txn)

    # Start the CLI
    cli(_anyio_backend="asyncio")
