
async def test_index_page(api):
    resp = await api.get('/')
    assert resp.status == 200
    body = await resp.text()
    assert len(body) > 0


async def test_moderate(api):
    payload = [{"comment": "xxx"}]
    resp = await api.post('/moderate', json=payload)
    assert resp.status == 200
    data = await resp.json()
    expected = [{
        'identity_hate': 0.01,
        'insult': 0.04,
        'obscene': 0.04,
        'severe_toxic': 0.01,
        'toxic': 0.1
    }]
    assert data == expected


async def test_validation_error(api):
    payload = [{"body": "xxx"}]
    resp = await api.post('/moderate', json=payload)
    assert resp.status == 400
    data = await resp.json()
    e = {'error': {'0': {'body': 'body is not allowed key',
                         'comment': 'is required'}}}
    assert data == e
