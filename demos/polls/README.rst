Polls (demo for aiohttp)
========================

Example of polls project using aiohttp_, aiopg_ and aiohttp_jinja2_,
similar to django one.

Installation
============

Prepare development environment
-------------------------------

We suggest you to start by creating an isolated Python working environment::

    $ python3 -m venv env
    $ source env/bin/activate


Install the app and it's requirements::

    $ cd demos/polls
    $ pip install -e .


Prepare database
----------------
Install Postgresql database server: http://www.postgresql.org/download/
(to use postgres in more isolated way you may also use docker. We will explain how to do that
after environment variables setup.)

Create ``.env`` file in ``polls`` folder with db related configuration values. It is a common practice to not
hardcode such settings because they differ between e.g. prod and dev environments::

    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=aiohttpdemo_polls
    DB_USER=aiohttpdemo_user
    DB_PASS=aiohttpdemo_user

Export these variables (to be able to use them inside db initializing script)::

    $ source .env
    $ export DB_HOST DB_PORT DB_NAME DB_USER DB_PASS

If you chose to use docker - here is the command for that (sure thing you need docker installed beforehand)::

    $ docker run --rm -it -p $DB_PORT:5432 postgres:10

Initialize db (if you started docker container - use separate shell for further commands).
It will create database, user, tables etc::

    $ bash sql/install.sh


Run
---
Run application::

    $ python -m aiohttpdemo_polls

Open browser::

    http://localhost:8080/

.. image:: https://raw.githubusercontent.com/andriisoldatenko/aiohttp_polls/master/images/example.png
    :align: center


Run integration tests::

  pip install tox
  tox


Requirements
============
* aiohttp_
* aiopg_
* aiohttp_jinja2_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _aiopg: https://github.com/aio-libs/aiopg
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2
