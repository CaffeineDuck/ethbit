import os
from click_configfile import (
    ConfigFileReader,
)
from pathlib import Path

import toml

__all__ = ("CONTEXT_SETTINGS",)


class ConfigFileProcessor(ConfigFileReader):
    @classmethod
    def read_config(cls):
        fullpath = Path.home() / ".ethbit/config.ini"
        if not os.path.exists(Path.home() / ".ethbit"):
            os.mkdir(Path.home() / ".ethbit")

        open(fullpath, "a").close()
        return toml.load(fullpath)


CONTEXT_SETTINGS = dict(default_map=ConfigFileProcessor.read_config())
