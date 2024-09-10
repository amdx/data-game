# Copyright (C) 2024 Archimedes Exhibitions GmbH,
# Saarbrücker Str. 24, Berlin, Germany
#
# This file contains proprietary source code and confidential
# information. Its contents may not be disclosed or distributed to
# third parties unless prior specific permission by Archimedes
# Exhibitions GmbH, Berlin, Germany is obtained in writing. This
# applies to copies made in any form and using any medium. It applies
# to partial as well as complete copies.
import functools
import os
import pathlib
import sys
from typing import Any, TextIO

from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from ruamel.yaml import YAML


class Config(BaseSettings):
    db_url: str
    data_path: pathlib.Path
    max_team_count: int
    max_card_count: int
    verify_ssl: bool = False
    log_levels: list[str] = ["root:warning"]

    # Note: The config keys can also be passed as arguments to the settings constructor.
    # Prefix the arguments with an underscore in that case.
    model_config = SettingsConfigDict(
        env_prefix="DASHBOARD_SERVICE_",
        extra="forbid",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    # Environment variables should have precedence over class init arguments.
    # Reference:
    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#changing-priority
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, init_settings, file_secret_settings


def build_default_config() -> Config:
    return Config(
        db_url="sqlite:///./workshop.db",
        data_path=pathlib.Path("examples/data.csv"),
        max_team_count=5,
        max_card_count=8,
        verify_ssl=False,
        log_levels=["root:warning"],
    )


def list_config_files() -> list[pathlib.Path]:
    config_files = []

    env_config = os.environ.get("DASHBOARD_SERVICE_CONFIG", None)
    if env_config is not None:
        config_files.append(pathlib.Path(env_config))

    config_files.extend(
        [
            pathlib.Path("dashboard_service.yaml"),
            pathlib.Path("dashboard_service.yml"),
            pathlib.Path("/etc/dashboard_service/dashboar_service.yaml"),
            pathlib.Path("/etc/dashboard_service/dashboar_service.yml"),
            pathlib.Path("/config/dashboard_service.yaml"),
            pathlib.Path("/config/dashboard_service.yml"),
        ]
    )
    return config_files


@functools.cache
def get_config() -> Config:
    for config_file in list_config_files():
        if config_file.exists():
            config_dict = read_config_file(config_file)
            config = Config(**config_dict)
            return config
    else:
        raise RuntimeError("No configuration file could be found.")


def read_config_file(config_file: pathlib.Path) -> dict[str, Any]:
    file_config = {}
    if config_file is not None:
        yml = YAML(typ="safe")
        with open(config_file) as f:
            file_config = yml.load(f)
    return file_config


def dump_config(config: Config, out: TextIO | None = None) -> None:
    # Use the pure python loader for better YAML output formatting
    yml = YAML(pure=True)
    yml.indent(mapping=2, sequence=4, offset=2)
    if out is None:
        yml.dump(config.model_dump(), sys.stdout)
    else:
        yml.dump(config.model_dump(), out)
