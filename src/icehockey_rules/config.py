import os
from functools import lru_cache
from pathlib import Path
from typing import Type, Annotated

from pydantic import Field, BaseModel, computed_field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
    SettingsConfigDict,
)

from icehockey_rules import config_dir, data_dir

CONFIG_FILEPATH = Path(os.getenv("CONFIG_FILEPATH", config_dir / "config.yaml"))


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


class LLM(BaseModel):
    model: str
    temperature: Annotated[float, Field(ge=0.0, le=1.0)]


class Retriever(BaseModel):
    top_k_chunks: Annotated[int, Field(gt=0)]
    top_k_rules: Annotated[int, Field(gt=0)]


class Embedder(BaseModel):
    model: str


class Splitter(BaseModel):
    max_chunk_size: int
    chunk_overlap: int


class Config(YamlBaseSettings):
    """Runtime config parser.

    The config loads parameters in the following order:

    1. passed to constructor
    2. from env vars
    3. from yaml file

    See Pydantic BaseSettings and/or FastAPI documentation for more information.
    """

    model_config = SettingsConfigDict(yaml_file=CONFIG_FILEPATH, strict=True, env_nested_delimiter="__")

    rulebooks_location: str

    llm: LLM
    retriever: Retriever
    embedder: Embedder
    splitter: Splitter

    system_prompt: str

    @computed_field
    @property
    def rulebooks_filepath(self) -> Path:
        rulebooks_filepath = Path(self.rulebooks_location)

        if len(rulebooks_filepath.parts) == 2:
            if rulebooks_filepath.parts[0] == "data_dir":
                rulebooks_filepath = data_dir / rulebooks_filepath.parts[1]

        if rulebooks_filepath.exists():
            return rulebooks_filepath

        raise ValueError(f"Could not resolve rulebooks filepath for {self.rulebooks_location}.")


@lru_cache
def get_config() -> Config:
    return Config()
