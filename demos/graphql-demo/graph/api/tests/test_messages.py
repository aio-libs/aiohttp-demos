import pytest


@pytest.mark.asyncio
async def test_simple_fetch_messages_from_room(client, requests):
    executed_rooms = await client.execute(
        """{
          rooms {
            id
          }
        }
        """,
        context_value=requests,
    )

    single_room = executed_rooms["data"]["rooms"][0]
    room_id = single_room["id"]

    executed_room = await client.execute(
        """{
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
        """
        % room_id,
        context_value=requests,
    )

    messages = executed_room["data"]["room"]["messages"]
    errors = executed_room["errors"]

    assert messages

    single_messages = messages[0]
    owner = single_messages["owner"]

    assert isinstance(single_messages["id"], int)
    assert not errors
    assert None not in owner.values()
    assert single_messages["body"]
    assert isinstance(owner["id"], int)
    assert owner["username"]
    assert owner["email"]
