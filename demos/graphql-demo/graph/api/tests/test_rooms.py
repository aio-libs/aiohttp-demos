import pytest


@pytest.mark.asyncio
async def test_simple_fetch_rooms(client, requests):
    executed = await client.execute(
        '''{
          rooms {
            id
            name
          }
        }
        ''',
        context_value=requests,
    )

    assert len(executed['data']['rooms']) == 1000

    single_room = executed['data']['rooms'][0]

    assert single_room['id'] == 1
    assert single_room['name'] == 'test#0'


@pytest.mark.asyncio
async def test_fetch_data_connected_with_owner_of_room(client, requests):
    executed = await client.execute(
        '''{
          rooms {
            owner {
              id
              username
              email
            }
          }
        }
        ''',
        context_value=requests,
    )

    owner = executed['data']['rooms'][0]['owner']

    assert owner['id']
    assert owner['username']
    assert owner['email']


@pytest.mark.asyncio
async def test_fetch_single_room(client, requests):
    executed = await client.execute(
        '''{
          rooms {
            id
            name
            owner {
              id
              username
              email
            }
          }
        }
        ''',
        context_value=requests,
    )

    single_room = executed['data']['rooms'][0]
    room_id = single_room['id']

    executed = await client.execute(
        '''{
          room(id: %s) {
            id
            name
            owner {
              id
              username
              email
            }
          }
        }
        ''' % room_id,
        context_value=requests,
    )

    assert executed['data']['room'] == single_room
