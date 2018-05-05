Polls
=====

Example of polls project using aiohttp_, aiopg_ and aiohttp_jinja2_,
similar to Django one.


Preparations
------------

Details could be found in `Preparations <https://github.com/aio-libs/aiohttp-demos/blob/master/docs/preparations.rst#environment>`_.

In short.

Run Postgres DB server::

    $ docker run --rm -it -p 5432:5432 postgres:10

Create db and populate it with sample data::

    $ python init_db.py


Run
---
Run application::

    $ python -m aiohttpdemo_polls

Open browser::

    http://localhost:8080/

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp-demos/master/docs/_static/polls.png
    :align: center
    :width: 460px

Tests
-----

.. code-block:: shell

    $ pytest tests

or:

.. code-block:: shell

    $ pip install tox
    $ tox


Development
-----------
Please review general contribution info at `README <https://github.com/aio-libs/aiohttp-demos#contributing>`_.


Also for illustration purposes it is useful to show project structure when it changes,
like `here <https://github.com/aio-libs/aiohttp-demos/blob/master/docs/preparations.rst#project-structure>`_.
Here is how you can do that::

    $ tree -I "__pycache__|aiohttpdemo_polls.egg-info" --dirsfirst


Requirements
============
* aiohttp_
* aiopg_
* aiohttp_jinja2_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _aiopg: https://github.com/aio-libs/aiopg
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2
