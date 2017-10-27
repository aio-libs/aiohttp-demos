Motortwit Demo
==============

Example of mongo project using aiohttp_, motor_ and aiohttp_jinja2_,
similar to flask one. Here I assume you have *python3.5* and *docker* installed.

Installation
============

Clone repo and install library::

    $ git clone git@github.com:aio-libs/aiohttp_admin.git
    $ cd aiohttp_admin
    $ pip install -e .
    $ pip install -r requirements-dev.txt

Install the app::

    $ cd demos/motortwit
    $ pip install -e .

Create database for your project::

    make docker_start_mongo
    make fake_data


Run application::

    $ make run

Open browser::

    http://127.0.0.1:9001/admin


Requirements
============
* aiohttp_
* motor_
* aiohttp_jinja2_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/KeepSafe/aiohttp
.. _motor: https://github.com/mongodb/motor
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2
