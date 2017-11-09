"""
Integration tests. They need a running database.

Beware, they destroy your db using sudo.
"""


async def test_index(cli):
    print('in test_index test')
    response = await cli.get('/poll/1')
    assert response.status == 200
    assert 'What\'s new?' in await response.text()

#
# async def test_results(cli):
#     response = await cli.get('/poll/1/results')
#     assert response.status == 200
#     assert 'Just hacking again' in await response.text()


#
# async def test_vote(cli):
#
#     from aiohttpdemo_polls.db import question, choice
#
#     async with cli.server.app['db'].acquire() as conn:
#         res = await conn.execute(choice.count())
#         print(await res.first())
#
#
#     response = await cli.post('/poll/1/vote', data={'choice': 1})
#     assert response.status == 200
#     # print(await response.text())
#
#
#     async with cli.server.app['db'].acquire() as conn:
#         res = await conn.execute(choice.count())
#         print(await res.first())
