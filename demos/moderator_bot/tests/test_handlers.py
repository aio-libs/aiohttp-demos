import hashlib
import hmac
import json
import time
from unittest import mock

import pytest


SIGNING_SECRET = "xxx"


def _sign(body, timestamp):
    basestring = b"v0:" + str(timestamp).encode() + b":" + body
    digest = hmac.new(
        SIGNING_SECRET.encode(), basestring, hashlib.sha256,
    ).hexdigest()
    return "v0=" + digest


async def _post_signed(client, payload, *, timestamp=None, signature=None):
    body = json.dumps(payload).encode()
    ts = str(timestamp if timestamp is not None else int(time.time()))
    sig = signature if signature is not None else _sign(body, ts)
    headers = {
        "Content-Type": "application/json",
        "X-Slack-Request-Timestamp": ts,
        "X-Slack-Signature": sig,
    }
    return await client.post("/listen", data=body, headers=headers)


async def test_listen_challenge(client):
    resp = await _post_signed(client, {"challenge": "challenge"})
    result = await resp.text()
    assert "challenge" in result


async def test_listen_message(client):
    with mock.patch('moderator_bot.handlers.MainHandler._respond') as m:
        await _post_signed(
            client,
            {
                "event": {
                    "type": "message",
                    "text": "You are stupid and useless!",
                    "user": "U012ABCDE",
                    "channel": "C012ABCDE",
                },
            },
        )
        assert m.called


async def test_listen_rejects_unsigned_request(client):
    resp = await client.post("/listen", json={"challenge": "challenge"})
    assert resp.status == 401


async def test_listen_rejects_bad_signature(client):
    resp = await _post_signed(
        client, {"challenge": "challenge"},
        signature="v0=" + "0" * 64,
    )
    assert resp.status == 401


async def test_listen_rejects_stale_timestamp(client):
    stale_ts = int(time.time()) - 60 * 10
    resp = await _post_signed(
        client, {"challenge": "challenge"}, timestamp=stale_ts,
    )
    assert resp.status == 401


@pytest.mark.parametrize("user, channel", [
    ("<script>alert(1)</script>", "C012ABCDE"),
    ("U012ABCDE", "C012; DROP TABLE"),
    ("u012abcde", "C012ABCDE"),
    ("U", "C012ABCDE"),
    ("", "C012ABCDE"),
])
async def test_listen_drops_event_with_invalid_slack_ids(
        client, user, channel):
    with mock.patch('moderator_bot.handlers.MainHandler._respond') as m, \
            mock.patch('moderator_bot.handlers.predict') as predict_mock:
        resp = await _post_signed(
            client,
            {
                "event": {
                    "type": "message",
                    "text": "anything",
                    "user": user,
                    "channel": channel,
                },
            },
        )
        assert resp.status == 200
        assert not predict_mock.called
        assert not m.called
