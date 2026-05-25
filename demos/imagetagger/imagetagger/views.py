import asyncio
from typing import Dict

import aiohttp_jinja2
from aiohttp import web
from PIL import Image, UnidentifiedImageError

from .constants import ALLOWED_CONTENT_TYPES, MAX_UPLOAD_BYTES
from .utils import Config
from .worker import predict


class SiteHandler:
    def __init__(self, conf: Config) -> None:
        self._conf = conf

    @aiohttp_jinja2.template('index.html')
    async def index(self, request: web.Request) -> Dict[str, str]:
        return {}

    async def predict(self, request: web.Request) -> web.Response:
        try:
            form = await request.post()
        except ValueError:
            raise web.HTTPBadRequest(reason="invalid form data")

        file_field = form.get('file')
        if not isinstance(file_field, web.FileField):
            raise web.HTTPBadRequest(reason="file field required")

        if file_field.content_type not in ALLOWED_CONTENT_TYPES:
            raise web.HTTPUnsupportedMediaType(
                reason="only image/jpeg and image/png uploads accepted")

        # Read one byte past the cap so we can distinguish "at limit" from
        # "over limit" without consuming the entire upload.
        raw_data = file_field.file.read(MAX_UPLOAD_BYTES + 1)
        file_field.file.close()  # Not needed in aiohttp 4+.
        if len(raw_data) > MAX_UPLOAD_BYTES:
            raise web.HTTPRequestEntityTooLarge(
                max_size=MAX_UPLOAD_BYTES, actual_size=len(raw_data))

        try:
            body = await asyncio.to_thread(predict, raw_data)
        except UnidentifiedImageError:
            raise web.HTTPBadRequest(reason="unsupported image format")
        except Image.DecompressionBombError:
            raise web.HTTPRequestEntityTooLarge(
                max_size=Image.MAX_IMAGE_PIXELS, actual_size=0,
                reason="image dimensions exceed pixel limit")

        headers = {'Content-Type': 'application/json'}
        return web.Response(body=body, headers=headers)
