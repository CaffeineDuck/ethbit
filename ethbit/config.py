from click_configfile import (
    ConfigFileReader,
)
from pathlib import Path

import toml

__all__ = ("CONTEXT_SETTINGS",)


class ConfigFileProcessor(ConfigFileReader):
    @classmethod
    def read_config(cls):
        return toml.load(Path.home() / ".ethbit/config.ini")


CONTEXT_SETTINGS = dict(default_map=ConfigFileProcessor.read_config())
