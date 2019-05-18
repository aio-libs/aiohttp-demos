import os
from pathlib import Path

import yaml


def load_config(path):
    with Path(path).open() as fp:
        return yaml.load(fp.read())


def required_env(variable):
    value = os.environ.get(variable)
    if value is None:
        raise RuntimeError(f"{variable} is required to start the service.")
    return value
