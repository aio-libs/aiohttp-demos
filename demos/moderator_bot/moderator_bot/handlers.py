from functools import partial

import numpy as np
from aiohttp import web

from .worker import predict


class MainHandler:
    def __init__(self, loop, executor, slack_client, giphy_client):
        self.loop = loop
        self.executor = executor
        self.slack_client = slack_client
        self.giphy_client = giphy_client
        self._toxicity_index = 0.4
        self._run = partial(self.loop.run_in_executor, self.executor)

    async def listen_message(self, request):
        post = await request.json()

        if "challenge" in post:
            return web.Response(body=post["challenge"])

        if post["event"]["type"] == "message":
            await self._message_handler(post["event"])

        return web.Response()

    async def _respond(self, event):
        result = await self.giphy_client.get(
            "random",
            params={
                "tag": "funny cat"
            },
        )
        image_url = result["data"]["image_url"]

        text = (f"Hey <@{event['user']}>, please be polite! "
                f"Here is a funny cat GIF for you {image_url}")

        await self.slack_client.chat.post_message(
            event["channel"],
            text=text,
        )

    async def _message_handler(self, event):
        scores = await self._run(predict, event["text"])
        if np.average([scores.toxic, scores.insult]) >= self._toxicity_index:
            await self._respond(event)
