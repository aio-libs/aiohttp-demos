Setup
=====

Terminal 1: Run db server::

    $ docker run --rm -it -p 5433:5432 postgres:10


(operating from base folder [../aiohttp-demos/demos/blog])

Terminal 2: Create db::

    $ python db_helpers.py -r

..db with tables and sample data::

    $ python db_helpers.py -a

Terminal 2: Check db for created data::

    $ psql -h localhost -p 5433 -U postgres -d aiohttpdemo_blog -c "select * from posts"

Terminal 3: Run server::

    $ python aiohttpdemo_blog/main.py -c config/user_config.toml


(example creds: Bob/bob)

Testing
=======

Run tests::

    $ pytest tests/test_stuff.py
