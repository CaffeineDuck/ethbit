import os
from pathlib import Path

import asyncclick as click
import toml


@click.command("setup", short_help="Setup config for ethbit.")
@click.option("--force", is_flag=True, help="Force overwriting the config file.")
def setup(force: bool) -> None:
    """
    Setup the config for ethbit
    """
    fullpath = Path.home() / ".ethbit/config.ini"
    config = {"main": {}}

    if os.path.exists(fullpath) and not force:
        raise click.UsageError("Config file already exists. Use --force to overwrite.")

    if not os.path.exists(fullpath):
        os.mkdir(Path.home() / ".ethbit")

    config["main"]["kraken_api_key"] = input("Enter Kraken API Key: ")
    config["main"]["kraken_api_sec"] = input("Enter Kraken API Secret: ")
    config["main"]["default_currency"] = input("Enter default currency: ")

    with open(fullpath, "w") as file_:
        file_.write(toml.dumps(config))

    click.echo(f"Config file created at {fullpath}")


@click.command("add", short_help="Add a new address to the config.")
@click.option(
    "--currency",
    required=True,
    help="The currency to add the address for.",
    type=click.Choice(["btc", "eth"]),
)
@click.option("--address", required=True, help="The address to add.")
@click.option("--name", required=True, help="The name to give the address.")
async def add(currency: str, address: str, name: str) -> None:
    """
    Add a new address to the config
    """
    fullpath = Path.home() / ".ethbit/config.ini"
    config = toml.load(fullpath)

    config[f"{currency}.{name}"] = {"name": name, "address": address}
    with open(fullpath, "w") as file:
        file.write(toml.dumps(config))

    click.echo(f"Address added for {currency}.")
