import argparse
import os
import pathlib

from dataclasses import dataclass
from typing import Any, Dict

import trafaret as t
from trafaret_config import commandline


PATH = pathlib.Path(__file__).parent.parent
settings_file = os.environ.get('SETTINGS_FILE', 'api.dev.yml')
DEFAULT_CONFIG_PATH = PATH / 'config' / settings_file


CONFIG_TRAFARET = t.Dict({
    t.Key('app'): t.Dict({
        t.Key('host'): t.String(),
        t.Key('port'): t.Int[0: 2 ** 16]
    }),
    t.Key('workers'): t.Dict({
        t.Key('model_path'): t.String,
    }),
})


@dataclass(frozen=True)
class AppConfig:
    host: str
    port: int


@dataclass(frozen=True)
class WorkersConfig:
    model_path: str


@dataclass(frozen=True)
class Config:
    app: AppConfig
    workers: WorkersConfig


def config_from_dict(d: Dict[str, Any]) -> Config:
    app_config = AppConfig(  # type: ignore
        host=d['app']['host'],
        port=d['app']['port'])
    workers_config = WorkersConfig(  # type: ignore
        model_path=d['workers']['model_path'],
    )
    return Config(app=app_config, workers=workers_config)  # type: ignore


def get_config(argv: Any = None) -> Config:
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap, default_config=DEFAULT_CONFIG_PATH
    )
    options = ap.parse_args(argv)
    d = commandline.config_from_options(options, CONFIG_TRAFARET)
    return config_from_dict(d)
