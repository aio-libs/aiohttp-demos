import pytest


@pytest.mark.asyncio
async def test_simple_fetch_messages_from_room(client, requests):
    executed = await client.execute(
        '''{
          rooms {
            id
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
            messages {
              id
              body
              favouriteCount
              owner {
                id
                email
                username
              }
            }
          }
        }
        ''' % room_id,
        context_value=requests,
    )

    messages = executed['data']['room']['messages']

    assert messages

    single_messages = messages[0]
    owner = single_messages['owner']

    assert isinstance(single_messages['id'], int)
    assert single_messages['body']
    assert isinstance(owner['id'], int)
    assert owner['username']
    assert owner['email']
