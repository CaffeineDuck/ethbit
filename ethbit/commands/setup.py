import os

import asyncclick as click
import toml

DEFAULT_CONFIG = {
    "path": "~/.config/status/",
}


@click.command("setup", short_help="Setup config for ethbit.")
@click.option("--path", default="~/.ethbit", help="The path to the config file.")
@click.option("--force", is_flag=True, help="Force overwriting the config file.")
def setup(path: str, force: bool) -> None:
    """
    Setup the config for ethbit
    """
    fullpath = path + "/config.toml"

    if os.path.exists(fullpath) and not force:
        click.echo("Config file already exists. Use --force to overwrite.", err=True)

    if not os.path.exists(path):
        os.mkdir(path)

    with open(fullpath, "w") as file_:
        file_.write(toml.dumps(DEFAULT_CONFIG))

    click.echo(f"Config file created at {fullpath}")
