import asyncclick as click

from ethbit.commands.balance import balance

from .commands.setup import setup


@click.group()
async def cli():
    ...


if __name__ == "__main__":
    # Add all the command groups
    cli.add_command(setup)
    cli.add_command(balance)

    # Start the CLI
    cli()
