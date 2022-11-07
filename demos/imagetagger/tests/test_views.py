from pathlib import Path

from aiohttp import FormData

DATA_PATH = Path(__file__).parent / "data"


async def test_index(api):
    resp = await api.get('/')

    assert resp.status == 200
    assert 'Imagetagger' in await resp.text()


async def test_predict(api):
    hotdog_path = DATA_PATH / "hotdog.jpg"
    img = hotdog_path.read_bytes()
    data = FormData()
    data.add_field(
        'file', img, filename='aircraft.jpg', content_type='image/img')

    resp = await api.post('/predict', data=data)
    assert resp.status == 200, resp
    data = await resp.json()
    assert data['success']
    assert data['predictions'][0]['label']
