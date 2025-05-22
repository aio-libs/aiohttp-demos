async def test_create_short_url(cli, clean_redis):
    """Test creating a short URL for a long URL."""
    long_url = "https://example.com/very/long/url/that/needs/shortening"

    async with cli.post("/shortify", json={"url": long_url}) as resp:
        await resp.read()
        assert resp.status == 200

    data = await resp.json()
    assert "url" in data
    assert data["url"] == "http://127.0.0.1:9001/a"


async def test_redirect_to_long_url(cli, clean_redis):
    """Test redirecting from short URL to original long URL."""
    long_url = "https://example.com/very/long/url/that/needs/shortening"

    # Create a short URL
    async with cli.post("/shortify", json={"url": long_url}) as resp:
        await resp.read()
        assert resp.status == 200
        data = await resp.json()
        short_url = data["url"]
        short_code = short_url.split("/")[-1]

    # Test the redirect
    async with cli.get(f"/{short_code}", allow_redirects=False) as resp:
        await resp.read()
        assert resp.status == 302
        assert resp.headers["Location"] == long_url


async def test_invalid_short_url(cli, clean_redis):
    """Test accessing a non-existent short URL."""
    async with cli.get("/nonexistent", allow_redirects=False) as resp:
        await resp.read()
        assert resp.status == 404
