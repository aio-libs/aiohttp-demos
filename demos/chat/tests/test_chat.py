import aiohttp
import pytest


async def test_msg_sending(client):
    ws1 = await client.ws_connect('/')
    ws2 = await client.ws_connect('/')

    ack_msg1 = await ws1.receive()
    assert ack_msg1.json()['action'] == 'connect'
    ack_msg2 = await ws2.receive()
    assert ack_msg2.json()['action'] == 'connect'

    text_to_send = 'hi all'
    await ws1.send_str(text_to_send)
    received_msg = await ws2.receive()
    received_dict = received_msg.json()

    assert set(received_dict) == {'action', 'name', 'text'}
    assert received_dict['text'] == text_to_send


async def test_chat_page_does_not_use_jquery_or_html_insertion(client):
    resp = await client.get('/')
    assert resp.status == 200

    page = await resp.text()

    assert 'jquery' not in page
    assert 'ajax.googleapis.com' not in page
    assert '.html(' not in page
    assert 'createTextNode' in page


async def test_ws_rejects_cross_origin(client):
    with pytest.raises(aiohttp.WSServerHandshakeError) as exc_info:
        await client.ws_connect(
            '/', headers={'Origin': 'http://evil.example'})
    assert exc_info.value.status == 403


async def test_ws_accepts_same_origin(client):
    origin = f'http://{client.host}:{client.port}'
    async with await client.ws_connect('/', headers={'Origin': origin}) as ws:
        msg = await ws.receive()
        assert msg.json()['action'] == 'connect'
