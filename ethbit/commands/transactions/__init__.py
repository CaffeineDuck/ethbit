import asyncclick as click
from .get_txn import get_transaction, save_transaction


@click.group("txn", help="Transaction commands")
def txn():
    ...


txn.add_command(get_transaction)
txn.add_command(save_transaction)
