import pathlib


OBJECT_NOT_FOUND_ERROR = 'Object not found'
PROJECT_DIR = pathlib.Path(__file__).parent.parent

# Cap raw upload size to limit the cost of decoding pathological inputs.
# 5 MiB comfortably covers normal photos while keeping the parser well
# inside RAM bounds.
MAX_UPLOAD_BYTES = 5 * 1024 * 1024

# Mirrors the frontend's <input accept="..."> attribute. Browsers send
# the file's content-type with the form part; reject anything that
# isn't an image up front so we don't even ask Pillow to look at it.
ALLOWED_CONTENT_TYPES = frozenset({"image/jpeg", "image/png"})
