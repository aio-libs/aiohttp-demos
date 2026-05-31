"""Tests for the per-subscription Redis pub/sub resolvers.

These drive the real resolver coroutines in
``graph.api.subscriptions.messages`` against a fake ``redis.asyncio``
client, so they need neither a running Redis nor the rest of the app.
The point the maintainer raised was the per-subscription connection
lifecycle: the resolver now uses ``async with client.pubsub()`` so the
dedicated connection is released when the subscriber goes away. The
``closed`` assertions below verify that the context manager actually
exits (i.e. the connection is cleaned up).
"""
import json
import types

from graph.api.subscriptions.messages import MessageSubscription


class _FakePubSub:
    """Stands in for a ``redis.asyncio`` PubSub, which is itself an async
    context manager (``async with client.pubsub() as ps``)."""

    def __init__(self, messages):
        self._messages = messages
        self.subscribed = []
        self.closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        self.closed = True
        return False

    async def subscribe(self, channel):
        self.subscribed.append(channel)

    async def listen(self):
        for message in self._messages:
            yield message


class _FakeRedis:
    def __init__(self, pubsub):
        self._pubsub = pubsub

    def pubsub(self):
        return self._pubsub


def _info_for(pubsub):
    app = {"redis_pub": _FakeRedis(pubsub)}
    request = types.SimpleNamespace(app=app)
    return types.SimpleNamespace(context={"request": request})


async def _drain(agen):
    return [item async for item in agen]


async def test_resolve_message_added_yields_and_releases_connection():
    pubsub = _FakePubSub([
        {"type": "subscribe", "data": 1},          # confirmation: skipped
        {"type": "message", "data": json.dumps({
            "body": "hello", "id": 7,
            "username": "ann", "user_id": 3})},
    ])
    sub = MessageSubscription()

    results = await _drain(
        sub.resolve_message_added(_info_for(pubsub), room_id=42))

    assert pubsub.subscribed == ["chat:42"]
    assert len(results) == 1            # the subscribe confirmation is dropped
    assert results[0].body == "hello"
    assert results[0].id == 7
    assert results[0].owner.username == "ann"
    assert results[0].owner.id == 3
    assert pubsub.closed is True        # connection released on exit


async def test_resolve_typing_start_yields_and_releases_connection():
    pubsub = _FakePubSub([
        {"type": "message", "data": json.dumps({"username": "bob", "id": 9})},
    ])
    sub = MessageSubscription()

    results = await _drain(
        sub.resolve_typing_start(_info_for(pubsub), room_id=5))

    assert pubsub.subscribed == ["chat:typing:5"]
    assert len(results) == 1
    assert results[0].user.username == "bob"
    assert results[0].user.id == 9
    assert pubsub.closed is True
