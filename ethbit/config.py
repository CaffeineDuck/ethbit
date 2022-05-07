from click_configfile import ConfigFileReader, Param, SectionSchema, matches_section

__all__ = ("CONTEXT_SETTINGS",)


class ConfigSectionSchema:
    @matches_section("main")
    class Main:
        currency = Param(default="USD")
        kraken_api_key = Param(type=str)
        kraken_api_sec = Param(type=str)

    @matches_section("eth.*")
    class Ethereum(SectionSchema):
        name = Param(type=str)
        address = Param(type=str)

    @matches_section("btc.*")
    class Bitcoin(SectionSchema):
        name = Param(type=str)
        address = Param(type=str)


class ConfigFileProcessor(ConfigFileReader):
    config_files = ["config.ini", "config.cfg"]
    config_section_schemas = [
        ConfigSectionSchema.Ethereum,
        ConfigSectionSchema.Bitcoin,
        ConfigSectionSchema.Main,
    ]


CONTEXT_SETTINGS = dict(default_map=ConfigFileProcessor.read_config())
