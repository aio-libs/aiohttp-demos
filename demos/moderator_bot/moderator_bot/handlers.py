import asyncio
import hashlib
import hmac
import json
import re
import time

import numpy as np
from aiohttp import web

from .worker import predict


# Slack object IDs are uppercase alphanumeric, 9+ chars, starting with a
# letter (e.g. U0123ABCDE, C0123ABCDE). The /listen handler validates
# event['user'] and event['channel'] against this before interpolating
# them into outbound Slack API calls.
_SLACK_ID_RE = re.compile(r"^[A-Z][A-Z0-9]{8,}$")

# Slack rejects request signatures with a timestamp older than this and
# we should too, to limit replay of captured-but-still-valid requests.
_SLACK_TIMESTAMP_MAX_SKEW_SECONDS = 60 * 5


class MainHandler:
    def __init__(self, executor, slack_client, giphy_client, signing_secret):
        self.executor = executor
        self.slack_client = slack_client
        self.giphy_client = giphy_client
        self._signing_secret = signing_secret.encode("utf-8")
        self._toxicity_index = 0.4

    def _verify_slack_signature(self, body, timestamp, signature):
        if not signature or not timestamp:
            return False
        try:
            ts = int(timestamp)
        except ValueError:
            return False
        if abs(time.time() - ts) > _SLACK_TIMESTAMP_MAX_SKEW_SECONDS:
            return False
        basestring = b"v0:" + timestamp.encode("utf-8") + b":" + body
        expected = "v0=" + hmac.new(
            self._signing_secret, basestring, hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    async def listen_message(self, request):
        body = await request.read()
        timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
        signature = request.headers.get("X-Slack-Signature", "")
        if not self._verify_slack_signature(body, timestamp, signature):
            raise web.HTTPUnauthorized(reason="invalid Slack signature")

        try:
            post = json.loads(body)
        except ValueError:
            raise web.HTTPBadRequest(reason="invalid JSON body")

        if "challenge" in post:
            return web.Response(body=post["challenge"])

        event = post.get("event") or {}
        if event.get("type") == "message":
            await self._message_handler(event)

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

        await self.slack_client.chat_postMessage(
            channel=event["channel"],
            text=text,
        )

    async def _message_handler(self, event):
        user = event.get("user", "")
        channel = event.get("channel", "")
        if not _SLACK_ID_RE.match(user) or not _SLACK_ID_RE.match(channel):
            return

        loop = asyncio.get_running_loop()
        scores = await loop.run_in_executor(
            self.executor, predict, event["text"])
        if np.average([scores.toxic, scores.insult]) >= self._toxicity_index:
            await self._respond(event)
