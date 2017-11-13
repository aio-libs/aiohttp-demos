Polls (demo for aiohttp)
========================

Example of polls project using aiohttp_, aiopg_ and aiohttp_jinja2_,
similar to Django one.


Preparations
------------

Run Postgres DB server::

    $ docker run --rm -it -p 5432:5432 postgres:10

Create db and populate it with sample data::

    $ python tests/init_db.py


Run
---
Run application::

    $ python -m aiohttpdemo_polls

Open browser::

    http://localhost:8080/

.. image:: https://raw.githubusercontent.com/andriisoldatenko/aiohttp_polls/master/images/example.png
    :align: center


Tests
-----

Run integration tests::

    $ pytest tests/test_integration.py

or::

    $ pip install tox
    $ tox


Requirements
============
* aiohttp_
* aiopg_
* aiohttp_jinja2_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _aiopg: https://github.com/aio-libs/aiopg
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2
