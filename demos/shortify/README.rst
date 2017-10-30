Shortify Demo
=============

Install the app::

    $ cd demos/shortify
    $ pip install -e .

Create database for your project::

    make docker_start_redis


Run application::

    $ make run

Open browser::

    http://127.0.0.1:9001


Requirements
============
* aiohttp_
* aiohttp_jinja2_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/KeepSafe/aiohttp
.. _motor: https://github.com/mongodb/motor
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2
