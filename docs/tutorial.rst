.. _aiohttp-tutorial:

Tutorial
========

Are you willing to learn *aiohttp* but don't know where to start?
**Polls** application, which is similar to the one in Django tutorial,
is a great example.
We will build something like:

.. image:: ../demos/polls/images/example.png
    :align: center


Getting started
---------------

aiohttp server is built around :class:`aiohttp.web.Application` instance.
It is used for registering *startup*/*cleanup* signals, connecting routes etc.

The following code creates an application::

    # main.py
    from aiohttp import web

    app = web.Application()
    web.run_app(app, host='127.0.0.1', port=8080)

Save it under ``aiohttpdemo_polls/main.py`` and start the server:

.. code-block:: shell

    $ python3 main.py
    ======== Running on http://127.0.0.1:8080 ========
    (Press CTRL+C to quit)

Open ``http://127.0.0.1:8080`` in browser... and it returns ``404: Not Found``.
To show something more meaningful let's create a route and a view.

.. _aiohttp-tutorial-views:

Views
-----

Let's start from first views. Create the file ``aiohttpdemo_polls/views.py``
with the following::

    # views.py
    from aiohttp import web

    async def index(request):
        return web.Response(text='Hello Aiohttp!')

This is the simplest view possible in Aiohttp. Now we should create a route
for this ``index`` view. Put this into ``aiohttpdemo_polls/routes.py``.
It is a good practice to separate views, routes, models etc.
You'll have more of each, and it is nice to have them in different places::

    # routes.py
    from views import index

    def setup_routes(app):
        app.router.add_get('/', index)


Also, we should call ``setup_routes`` function somewhere, and the best place
is in the ``main.py`` ::

   # main.py
   from aiohttp import web
   from routes import setup_routes

   app = web.Application()
   setup_routes(app)
   web.run_app(app, host='127.0.0.1', port=8080)

Start server again. Now if we open browser we can see::

    Hello Aiohttp!

Success! For now your working directory should look like this:

.. code-block:: none

    .
    ├── ..
    └── polls
        └── aiohttpdemo_polls
            ├── main.py
            ├── routes.py
            └── views.py


.. _aiohttp-tutorial-config:

Configuration files
-------------------

.. note::

    aiohttp is configuration agnostic. It means the library does not
    require any configuration approach and does not have builtin support
    for any config schema.

    But please take into account these facts:

       1. 99% of servers have configuration files.

       2. Most products (except Python-based solutions like Django and
          Flask) do not store configs with source code.

          For example Nginx has own configuration files stored by default
          under ``/etc/nginx`` folder.

          Mongo pushes config as ``/etc/mongodb.conf``.

       3. Config files validation is good idea, strong checks may prevent
          silly errors during product deployment.

    Thus we **suggest** to use the following approach:

       1. Pushing configs as ``yaml`` files (``json`` or ``ini`` is also
          good but ``yaml`` is the best).

       2. Loading ``yaml`` config from a list of predefined locations,
          e.g. ``./config/app_cfg.yaml``, ``/etc/app_cfg.yaml``.

       3. Keeping ability to override config file by command line
          parameter, e.g. ``./run_app --config=/opt/config/app_cfg.yaml``.

       4. Applying strict validation checks to loaded dict. `trafaret
          <http://trafaret.readthedocs.io/en/latest/>`_, `colander
          <http://docs.pylonsproject.org/projects/colander/en/latest/>`_
          or `JSON schema
          <http://python-jsonschema.readthedocs.io/en/latest/>`_ are good
          candidates for such job.


One way to store your config is in folder at the same level as `aiohttpdemo_polls`.
Create config folder and config file at desired location. E.g.:

.. code-block:: none

    .
    ├── ..
    └── polls                   <-- [BASE_DIR]
        │
        ├── aiohttpdemo_polls
        │   ├── main.py
        │   ├── routes.py
        │   └── views.py
        │
        └── config
            └── polls.yaml      <-- [config file]

Create ``config/polls.yaml`` file with database schemas

.. code-block:: yaml

    # polls.yaml
    postgres:
      database: aiohttpdemo_polls
      user: aiohttpdemo_user
      password: aiohttpdemo_pass
      host: localhost
      port: 5432
      minsize: 1
      maxsize: 5

    host: 127.0.0.1
    port: 8080

Install ``pyyaml``::

    $ pip install pyyaml

And now load config into the application::

    # main.py
    import pathlib

    from aiohttp import web
    import yaml
    from routes import setup_routes


    BASE_DIR = pathlib.Path(__file__).parent.parent
    config_path = BASE_DIR / 'config' / 'polls.yaml'
    with open(config_path) as f:
        config = yaml.load(f)

    app = web.Application()
    setup_routes(app)
    app['config'] = config
    web.run_app(app, host='127.0.0.1', port=8080)


Try to run your app again. Make sure you are running it from ``BASE_DIR``::

    $ python aiohttpdemo_polls/main.py
    ======== Running on http://127.0.0.1:8080 ========
    (Press CTRL+C to quit)

For the moment nothing should have changed in application's behavior. But at
least we know how to configure our application.


.. _aiohttp-tutorial-database:

Database
--------

Schema
^^^^^^

We will use SQLAlchemy to describe database schema for two related models,
``question`` and ``choice``::

    +---------------+               +---------------+
    | question      |               | choice        |
    +===============+               +===============+
    | id            | <---+         | id            |
    +---------------+     |         +---------------+
    | question_text |     |         | choice_text   |
    +---------------+     |         +---------------+
    | pub_date      |     |         | votes         |
    +---------------+     |         +---------------+
                          +-------- | question_id   |
                                    +---------------+

Create ``db.py`` file with database schemas ::

    # db.py
    from sqlalchemy import (
        MetaData, Table, Column, ForeignKey,
        Integer, String, Date
    )

    meta = MetaData()

    question = Table(
        'question', meta,

        Column('id', Integer, primary_key=True),
        Column('question_text', String(200), nullable=False),
        Column('pub_date', Date, nullable=False)
    )

    choice = Table(
        'choice', meta,

        Column('id', Integer, primary_key=True),
        Column('question_id', Integer, nullable=False),
        Column('choice_text', String(200), nullable=False),
        Column('votes', Integer, server_default="0", nullable=False),

        Column('question_id',
               Integer,
               ForeignKey('question.id', ondelete='CASCADE'))
    )


.. note::

    It is possible to configure tables in declarative style like so:

    .. code-block:: python

        class Question(Base):
            __tablename__ = 'question'

            id = Column(Integer, primary_key=True)
            question_text = Column(String(200), nullable=False)
            pub_date = Column(Date, nullable=False)


    But it doesn't give much benefits later on. SQLAlchemy ORM doesn't work in
    asynchronous style and as a result ``aiopg.sa`` doesn't support related ORM
    expressions such as ``Question.query.filter_by(question_text='Why').first()``
    or ``session.query(TableName).all()``.

    You still can make select queries after little code modifications:

    .. code-block:: python

        from sqlalchemy.sql import select
        result = await conn.execute(select([Question]))

    instead of

    .. code-block:: python

            result = await conn.execute(question.select())

    But it is not so easy to deal with update/delete queries.


Creating connection engine
^^^^^^^^^^^^^^^^^^^^^^^^^^

For making DB queries we need an engine instance. Assuming ``conf`` is
a :class:`dict` with configuration info Postgres connection could be
done by the following coroutine:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/db.py
  :pyobject: init_pg

The best place for connecting to DB is
:attr:`~aiohtp.web.Application.on_startup` signal::

   app.on_startup.append(init_pg)


Graceful shutdown
^^^^^^^^^^^^^^^^^

There is a good practice to close all resources on program exit.

Let's close DB connection in :attr:`~aiohtp.web.Application.on_cleanup` signal::

    app.on_cleanup.append(close_pg)


.. literalinclude:: ../demos/polls/aiohttpdemo_polls/db.py
  :pyobject: close_pg


.. _aiohttp-tutorial-templates:

Templates
---------

Let's add more useful views:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/views.py
  :pyobject: poll

Templates are very convenient way for web page writing. We return a
dict with page content, ``aiohttp_jinja2.template`` decorator
processes it by jinja2 template renderer.

For setting up template engine we need to install ``aiohttp_jinja2``
library first:

.. code-block:: shell

   $ pip install aiohttp_jinja2

After installing we need to setup the library::

    import aiohttp_jinja2
    import jinja2

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('aiohttpdemo_polls', 'templates'))


In the tutorial we push template files under
``polls/aiohttpdemo_polls/templates`` folder.


.. _aiohttp-tutorial-static:

Static files
------------

Any web site has static files: images, JavaScript sources, CSS files etc.

The best way to handle static in production is setting up reverse
proxy like NGINX or using CDN services.

But for development handling static files by aiohttp server is very convenient.

Fortunately it can be done easy by single call:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/routes.py
  :pyobject: setup_static_routes

where ``project_root`` is the path to root folder.


.. _aiohttp-tutorial-middlewares:

Middlewares
-----------

Middlewares are stacked around every web-handler.  They are called
*before* handler for pre-processing request and *after* getting
response back for post-processing given response.

Here we'll add a simple middleware for displaying pretty looking pages
for *404 Not Found* and *500 Internal Error*.

Middlewares could be registered in ``app`` by adding new middleware to
``app.middlewares`` list:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/middlewares.py
  :pyobject: setup_middlewares

Middleware itself is a factory which accepts *application* and *next
handler* (the following middleware or *web-handler* in case of the
latest middleware in the list).

The factory returns *middleware handler* which has the same signature
as regular *web-handler* -- it accepts *request* and returns
*response*.

Middleware for processing HTTP exceptions:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/middlewares.py
  :pyobject: error_pages

Registered overrides are trivial Jinja2 template renderers:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/middlewares.py
  :pyobject: handle_404

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/middlewares.py
  :pyobject: handle_500

.. seealso:: :ref:`aiohttp-web-middlewares`
