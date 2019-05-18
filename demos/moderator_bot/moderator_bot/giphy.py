from functools import partialmethod

import aiohttp
import async_timeout
from yarl import URL


class GiphyClient:
    def __init__(self, loop, api_key, timeout, session=None):
        self.loop = loop
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = URL("https://api.giphy.com/v1/gifs")

        if session is None:
            session = aiohttp.ClientSession(loop=self.loop)

        self.session = session

    async def _request(self, method, part, *args, **kwargs):
        url = self.base_url / part

        kwargs.setdefault("params", {})
        kwargs["params"] = {
            "api_key": self.api_key,
            **kwargs["params"]
        }

        async with async_timeout.timeout(self.timeout):
            async with self.session.request(
                method,
                url,
                *args,
                **kwargs
            ) as resp:
                if "application/json" in resp.content_type:
                    return await resp.json()

    get = partialmethod(_request, "GET")

    async def close(self):
        await self.session.close()
