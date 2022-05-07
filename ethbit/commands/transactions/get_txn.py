import json
import asyncclick as click
from ethbit import w3
from rich import print
from asyncclick.core import Context

from ethbit.commands.balance.utils import CurrType, get_stored_addresses
from ethbit.commands.transactions.models import Transaction


@click.command("get")
@click.argument("address", required=False)
@click.option("--name", "-n", type=str, help="Name of the address", required=False)
@click.option(
    "--file",
    "-f",
    type=click.File(mode="r"),
    help="File to get the stored address",
    required=False,
)
@click.pass_context
async def get_transaction(
    ctx: Context, address: str | None, name: str | None, file: click.File | None
):
    if file is not None:
        with open(file.name, "r") as f:
            return print(json.loads(f.read()))

    if address and name:
        raise click.BadArgumentUsage("You can only specify one of the arguments")

    if name:
        address = get_stored_addresses(ctx.default_map, CurrType.ETH, name)[0]

    if not address:
        raise click.BadArgumentUsage("You must specify an address")

    transactions = get_transactions(address)
    print([tx.dict() for tx in transactions])


@click.command("save")
@click.argument("address", required=False)
@click.option("--name", type=str, help="Name of the address", required=False)
@click.option(
    "--file",
    type=click.Path(exists=True),
    help="Path to the file to save the transactions to",
    required=True,
)
@click.pass_context
async def save_transaction(
    ctx: Context, address: str | None, name: str | None, file: click.Path
):
    if address and name:
        raise click.BadArgumentUsage("You can only specify one of the arguments")

    if name:
        address = get_stored_addresses(ctx.default_map, CurrType.ETH, name)[0]

    if not address:
        raise click.BadArgumentUsage("You must specify an address")

    if not file:
        raise click.BadArgumentUsage("You must specify a file")

    transactions = [txn.dict() for txn in get_transactions(address)]

    with open(f"{file}/{address}.json", "w") as f:
        f.write(json.dumps(transactions, indent=4, sort_keys=True))

    click.echo("File written successfully")


def get_transactions(address: str):
    latest_block = w3.eth.get_block("latest")
    txns = []
    while True:
        for tx in latest_block.get("transactions"):  # type: ignore
            new_tx = w3.eth.get_transaction(tx)  # type: ignore
            if new_tx.get("from") == address or new_tx.get("to") == address:
                txns.append(Transaction(**new_tx))  # type: ignore
        try:
            latest_block = w3.eth.get_block(latest_block.get("parentHash"))  # type: ignore
        except ValueError:
            break

    return txns
