Setup
=====

Clone the repo, create virtualenv if necessary.

Operate from base folder [../aiohttp-demos/demos/blog].

To start the demo application you need running Postgres server.
In case you have it already - good.

But if you want neither to use it for experiments nor to stop the server:
- update DB_PORT in config files
- use desired port in following example commands e.g. like so::

    $ export DB_PORT=5433

Run db servers::

    $ docker run --rm -d -p $DB_PORT:5432 postgres:10
    $ docker run --rm -d -p 6379:6379 redis


Create db with tables and sample data::

    $ python db_helpers.py -a

Check db for created data::

    $ psql -h localhost -p $DB_PORT -U postgres -d aiohttpdemo_blog -c "select * from posts"

Run server::

    $ python aiohttpdemo_blog/main.py -c config/user_config.toml


(example creds: Bob/bob)

Testing
=======

Run tests::

    $ pytest tests/test_stuff.py
