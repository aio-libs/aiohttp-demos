import pytest
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_create_short_url(cli, clean_redis):  
    """Test creating a short URL for a long URL."""
    long_url = "https://example.com/very/long/url/that/needs/shortening"
    
    resp = await cli.post('/shortify', json={'url': long_url})
    assert resp.status == 200
    
    data = await resp.json()
    assert 'url' in data
    assert data['url'].startswith('http://')
    assert len(data['url'].split('/')[-1]) == 1


@pytest.mark.asyncio
async def test_redirect_to_long_url(cli, clean_redis):
    """Test redirecting from short URL to original long URL."""
    long_url = "https://example.com/very/long/url/that/needs/shortening"
    
    # Create a short URL
    resp = await cli.post('/shortify', json={'url': long_url})
    assert resp.status == 200
    data = await resp.json()
    short_url = data['url']
    short_code = short_url.split('/')[-1]
    
    # Test the redirect
    resp = await cli.get(f'/{short_code}', allow_redirects=False)
    assert resp.status == 302
    assert resp.headers['Location'] == long_url



@pytest.mark.asyncio
async def test_invalid_short_url(cli, clean_redis):     
    """Test accessing a non-existent short URL."""
    resp = await cli.get('/nonexistent', allow_redirects=False)
    assert resp.status == 404
