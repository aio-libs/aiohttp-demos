from unittest import mock


async def test_listen_challenge(client):
    resp = await client.post("/listen", json={"challenge": "challenge"})
    result = await resp.text()
    assert "challenge" in result


async def test_list_message(client):
    with mock.patch('moderator_bot.handlers.MainHandler._respond') as m:
        await client.post(
            "/listen",
            json={
                "event": {
                    "type": "message",
                    "text": "You are stupid and useless!"
                },
            },
        )
        assert m.called
