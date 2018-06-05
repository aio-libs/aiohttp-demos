Setup
=====

Terminal 1: Run db server::

    $ docker run --rm -it -p 5433:5432 postgres:10


(operating from base folder [../aiohttp-demos/demos/blog])

Terminal 2: Create db::

    $ python db_helpers.py -r

..db with tables and sample data::

    $ python db_helpers.py -a


Terminal 3: Run server::

    $ python aiohttpdemo_blog/main.py -c config/user_config.toml


(example creds: Bob/bob)

Testing
=======

Run tests::

    $ pytest tests/test_stuff.py
