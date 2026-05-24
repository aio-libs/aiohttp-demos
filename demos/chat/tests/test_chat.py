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
