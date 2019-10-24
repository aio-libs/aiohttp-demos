import pytest


@pytest.mark.asyncio
async def test_mutations_for_message(client, requests):
    text = 'test messages'
    room_id = 1
    owner_id = 1

    async def fetch_messages(room_id: int):
        return await client.execute(
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

    executed = await fetch_messages(room_id)
    messages = executed['data']['room']['messages']
    init_last_messages = messages[-1]

    executed = await client.execute(
        '''
          mutation {
            addMessage(roomId: %s, ownerId: %s, body: "%s") {
              isCreated
            }
          }
        ''' % (room_id, owner_id, text),
        context_value=requests,
    )

    assert executed['data']['addMessage']['isCreated']

    executed = await fetch_messages(room_id)
    messages = executed['data']['room']['messages']
    last_messages = messages[-1]

    assert last_messages['owner']['id'] == owner_id
    assert last_messages['body'] == text

    executed = await client.execute(
        '''
          mutation {
            removeMessage(id: %s) {
              isRemoved
            }
          }
        ''' % last_messages['id'],
        context_value=requests,
    )

    assert executed['data']['removeMessage']['isRemoved']

    executed = await fetch_messages(room_id)
    messages = executed['data']['room']['messages']
    last_messages = messages[-1]

    assert last_messages == init_last_messages
