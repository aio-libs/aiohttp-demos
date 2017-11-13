Preparations
============

You may start with empty folder and create files alongside with the
tutorial.
In the end project structure will look very similar to other python based
web projects:

.. code-block:: none

    .
    ├── Makefile
    ├── README.rst
    ├── aiohttpdemo_polls
    │   ├── static
    │   │   └── style.css
    │   ├── templates
    │   │   ├── 404.html
    │   │   ├── 500.html
    │   │   ├── base.html
    │   │   ├── detail.html
    │   │   ├── index.html
    │   │   └── results.html
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── db.py
    │   ├── main.py
    │   ├── middlewares.py
    │   ├── routes.py
    │   ├── utils.py
    │   └── views.py
    ├── config
    │   ├── polls.yaml
    │   └── polls_test.yaml
    ├── images
    │   └── example.png
    ├── requirements.txt
    ├── setup.py
    └── tests
        ├── __init__.py
        ├── conftest.py
        ├── init_db.py
        └── test_integration.py


If you want the full source code in advance or for comparison,
check out the `demo source`_.

.. _demo source:
   https://github.com/aio-libs/aiohttp-demos/tree/master/demos/polls/


Environment
-----------
We suggest you to start by creating an isolated Python environment::

    $ python3 -m venv env
    $ source env/bin/activate


Install the app and it's requirements::

    $ cd demos/polls
    $ pip install -e .


Check you python version (tutorial requires Python 3.5 or newer)::

   $ python -V
   Python 3.6.3

Also check the aiohttp version by running the following command::

   $ python3 -c 'import aiohttp; print(aiohttp.__version__)'
   2.3.1


Database
--------
We could have created this tutorial based on local ``sqlite`` solution,
but it is almost never used in real-world applications.
So we decided to use Postgres.

Install and run Postgresql database server: http://www.postgresql.org/download/
To use Postgres in more isolated way you may also use Docker::

    $ docker run --rm -it -p 5432:5432 postgres:10

Create db at running server, create tables and populate them with sample data::

    $ python tests/init_db.py

