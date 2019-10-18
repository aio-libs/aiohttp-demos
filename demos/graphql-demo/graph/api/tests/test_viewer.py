import pytest


@pytest.mark.asyncio
async def test_viewer(client, requests):
    executed = await client.execute(
        """
        {
          viewer {
            id
          }
        }
        """,
        return_value=requests,
    )

    assert executed['data']['viewer'] is None
