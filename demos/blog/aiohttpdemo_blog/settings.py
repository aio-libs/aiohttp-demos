import pathlib
import pytoml as toml

BASE_DIR = pathlib.Path(__file__).parent.parent
PACKAGE_NAME = 'aiohttpdemo_blog'


def load_config(path):
    with open(path) as f:
        conf = toml.load(f)
    return conf
