import asyncclick as click

from ethbit.commands.balance import balance
from ethbit.commands.transactions import txn
from click_rich_help import StyledGroup

from .commands.setup import setup


@click.group(cls=StyledGroup)
async def cli():
    ...


if __name__ == "__main__":
    # Add all the command groups
    cli.add_command(setup)
    cli.add_command(balance)
    cli.add_command(txn)

    # Start the CLI
    cli()
