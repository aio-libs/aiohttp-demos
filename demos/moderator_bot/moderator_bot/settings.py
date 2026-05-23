import os
from pathlib import Path

from .utils import required_env

PROJECT_ROOT = Path(__file__).parent.parent

MAX_WORKERS = os.cpu_count()

SLACK_BOT_TOKEN = required_env("SLACK_BOT_TOKEN")

SLACK_SIGNING_SECRET = required_env("SLACK_SIGNING_SECRET")

GIPHY_API_KEY = required_env("GIPHY_API_KEY")
