import sys
from pathlib import Path

from moderator.consts import PROJ_ROOT
from moderator.model.pipeline import build_model


if __name__ == '__main__':
    dataset_path = Path(sys.argv[1])
    model_path = PROJ_ROOT / 'model'
    build_model(dataset_path, model_path)
