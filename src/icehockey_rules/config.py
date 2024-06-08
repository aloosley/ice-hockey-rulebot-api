import os
from pathlib import Path
from typing import Type, Annotated

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
    SettingsConfigDict,
)

from icehockey_rules import config_dir

CONFIG_FILEPATH = Path(os.getenv("CONFIG_FILEPATH", config_dir / "config.yml"))


class YamlBaseSettings(BaseSettings):
    """BaseSettings class designed to load yaml files.

    Note, all variables can be overridden from env.
    For nested variables, set an `env_nested_delimiter` in model_config.
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, YamlConfigSettingsSource(settings_cls)


class Config(YamlBaseSettings):
    """Runtime config parser.

    The config loads parameters in the following order:

    1. passed to constructor
    2. from env vars
    3. from yaml file

    See Pydantic BaseSettings and/or FastAPI documentation for more information.
    """

    model_config = SettingsConfigDict(yaml_file=CONFIG_FILEPATH, strict=True, env_nested_delimiter="__")

    llm_model: str
    llm_temperature: Annotated[float, Field(ge=0.0, le=1.0)]
    embedder_model: str

    system_prompt: str
