from aiohttp import FormData

from imagetagger.constants import MAX_UPLOAD_BYTES


async def test_predict_rejects_disallowed_content_type(api):
    data = FormData()
    data.add_field(
        'file', b'GIF89a\x00', filename='x.gif', content_type='image/gif')

    resp = await api.post('/predict', data=data)
    assert resp.status == 415, resp


async def test_predict_rejects_missing_file_field(api):
    data = FormData()
    data.add_field('other', 'value')

    resp = await api.post('/predict', data=data)
    assert resp.status == 400, resp


async def test_predict_rejects_oversized_upload(api):
    payload = b'\xff' * (MAX_UPLOAD_BYTES + 1)
    data = FormData()
    data.add_field(
        'file', payload, filename='big.jpg', content_type='image/jpeg')

    resp = await api.post('/predict', data=data)
    assert resp.status == 413, resp


async def test_predict_rejects_non_image_bytes(api):
    data = FormData()
    data.add_field(
        'file', b'not really a jpeg', filename='x.jpg',
        content_type='image/jpeg')

    resp = await api.post('/predict', data=data)
    assert resp.status == 400, resp
