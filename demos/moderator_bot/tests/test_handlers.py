async def test_listen_challenge(client):
    resp = await client.post("/listen", json={"challenge": "challenge"})
    result = await resp.text()
    assert "challenge" in result


async def test_list_message(client):
    await client.post(
        "/list",
        json={
            "event": {
                "type": "message",
                "text": "test"
            },
        },
    )
