.. _aiohttp-demos-polls-getting-started:

Getting started
---------------

Let's start with basic folder structure:

    - project folder named ``polls``. A root of the project. Run all commands from here.
    - application folder named ``aiohttpdemo_polls`` inside of it
    - empty file ``main.py``. The place where web server will live

We need this nested ``aiohttpdemo_polls`` so we can put config, tests and other related
files next to it.

It looks like this:

.. code-block:: none

     polls                   <-- [current folder]
     └── aiohttpdemo_polls
         └── main.py


aiohttp server is built around :class:`aiohttp.web.Application` instance.
It is used for registering *startup*/*cleanup* signals, connecting routes etc.

The following code creates an application:

.. code-block:: python

    # aiohttpdemo_polls/main.py
    from aiohttp import web

    app = web.Application()
    web.run_app(app)

Save it and start server by running:

.. code-block:: shell

    $ python aiohttpdemo_polls/main.py
    ======== Running on http://0.0.0.0:8080 ========
    (Press CTRL+C to quit)

Next, open the displayed link in a browser. It returns a ``404: Not Found``
error. To show something more meaningful than an error, let's create a route
and a view.


.. _aiohttp-demos-polls-views:

Views
-----

Let's start with the first views. Create the file ``aiohttpdemo_polls/views.py``
and add the following to it:

.. code-block:: python

    # aiohttpdemo_polls/views.py
    from aiohttp import web

    async def index(request):
        return web.Response(text='Hello Aiohttp!')

This ``index`` view is the simplest view possible in Aiohttp.

Now, we should create a route for this ``index`` view. Put the following into
``aiohttpdemo_polls/routes.py``. It is a good practice to separate views,
routes, models etc. You'll have more of each file type, and it is nice to group
them into different places:

.. code-block:: python

    # aiohttpdemo_polls/routes.py
    from views import index

    def setup_routes(app):
        app.router.add_get('/', index)


We should add a call to the ``setup_routes`` function somewhere. The best place
to do this is in ``main.py``:

.. code-block:: python

   # aiohttpdemo_polls/main.py
   from aiohttp import web
   from routes import setup_routes

   app = web.Application()
   setup_routes(app)
   web.run_app(app)

Start server again using ``python aiohttpdemo_polls/main.py``. This time when we open the browser
we see::

    Hello Aiohttp!

**Success!** Now, your working directory should look like this:

.. code-block:: none

    .
    ├── ..
    └── polls
        └── aiohttpdemo_polls
            ├── main.py
            ├── routes.py
            └── views.py


.. _aiohttp-demos-polls-configuration-files:

Configuration files
-------------------

.. note::

    aiohttp is configuration agnostic. It means the library does not
    require any specific configuration approach, and it does not have built-in
    support for any config schema.

    Please note these facts:

       1. 99% of servers have configuration files.

       2. Most products (except Python-based solutions like Django and
          Flask) do not store configs with source code.

          For example Nginx has its own configuration files stored by default
          under ``/etc/nginx`` folder.

          MongoDB stores its config as ``/etc/mongodb.conf``.

       3. Config file validation is a good idea. Strong checks may prevent
          unnecessary errors during product deployment.

    Thus, we **suggest** to use the following approach:

       1. Push configs as ``yaml`` files (``json`` or ``ini`` is also
          good but ``yaml`` is preferred).

       2. Load ``yaml`` config from a list of predefined locations,
          e.g. ``./config/app_cfg.yaml``, ``/etc/app_cfg.yaml``.

       3. Keep the ability to override a config file by a command line
          parameter, e.g. ``./run_app --config=/opt/config/app_cfg.yaml``.

       4. Apply strict validation checks to loaded dict. `trafaret
          <http://trafaret.readthedocs.io/en/latest/>`_, `colander
          <http://docs.pylonsproject.org/projects/colander/en/latest/>`_
          or `JSON schema
          <http://python-jsonschema.readthedocs.io/en/latest/>`_ are good
          candidates for such job.


One way to store your config is in folder at the same level as `aiohttpdemo_polls`.
Create a ``config`` folder and config file at desired location. E.g.:

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

Create a ``config/polls.yaml`` file with meaningful option names:

.. code-block:: yaml

    # config/polls.yaml
    postgres:
      database: aiohttpdemo_polls
      user: aiohttpdemo_user
      password: aiohttpdemo_pass
      host: localhost
      port: 5432
      minsize: 1
      maxsize: 5

Install ``pyyaml`` package::

    $ pip install pyyaml

Let's also create a separate ``settings.py`` file. It helps to leave ``main.py``
clean and short:

.. code-block:: python

    # aiohttpdemo_polls/settings.py
    import pathlib
    import yaml

    BASE_DIR = pathlib.Path(__file__).parent.parent
    config_path = BASE_DIR / 'config' / 'polls.yaml'

    def get_config(path):
        with open(path) as f:
            config = yaml.safe_load(f)
        return config

    config = get_config(config_path)


Next, load the config into the application:

.. code-block:: python
    :emphasize-lines: 8

    from aiohttp import web

    from settings import config
    from routes import setup_routes

    app = web.Application()
    setup_routes(app)
    app['config'] = config
    web.run_app(app)

Now, try to run your app again. Make sure you are running it from ``BASE_DIR``::

    $ python aiohttpdemo_polls/main.py
    ======== Running on http://0.0.0.0:8080 ========
    (Press CTRL+C to quit)

For the moment nothing should have changed in application's behavior. But at least we
know how to configure our application.


.. _aiohttp-demos-polls-database:

Database
--------

Server
^^^^^^
Here, we assume that you have running database and a user with write access.
Refer to :ref:`aiohttp-demos-polls-preparations-database` for details.

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

Create ``db.py`` file with database schemas:

.. code-block:: python

    from sqlalchemy import MetaData, ForeignKey, String
    from sqlalchemy.orm import declarative_base, Mapped, mapped_column
    from datetime import date

    Base = declarative_base()

    class Question(Base):
        __tablename__ = "question"

        id: Mapped[int] = mapped_column(primary_key=True)
        question_text: Mapped[str] = mapped_column(String(200), nullable=False)
        pub_date: Mapped[date]

    class Choice(Base):
        __tablename__ = "choice"

        id: Mapped[int] = mapped_column(primary_key=True)
        choice_text: Mapped[str] = mapped_column(String(200), nullable=False)
        votes: Mapped[int] = mapped_column(server_default="0", nullable=False)

        question_id: Mapped[int] = mapped_column(
            ForeignKey('question.id', ondelete='CASCADE')
        )


Now we need to create tables in database as it was described with sqlalchemy.
Helper script can do that for you. Create a new file ``init_db.py`` in project's root:

.. code-block:: python

    from sqlalchemy import create_engine, MetaData
    from sqlalchemy.orm import Session, sessionmaker
    from datetime import date

    from aiohttpdemo_polls.settings import config
    from aiohttpdemo_polls.db import Question, Choice, Base
    
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

    def create_tables(engine):
        Base.metadata.create_all(bind=engine)

    def sample_data(engine):
        Session = sessionmaker(engine)
        with Session.begin() as session:
            session.add_all((
                Question(question_text="What\'s new?",pub_date=date(2015, 12, 15)),
                Choice(choice_text="Not much", votes=0, question_id=1),
                Choice(choice_text="The sky", votes=0, question_id=1),
                Choice(choice_text="Just hacking again", votes=0, question_id=1)
            ))

    if __name__ == "__main__":
        db_url = DSN.format(**config["postgres"])
        engine = create_engine(db_url)

        create_tables(engine)
        sample_data(engine)

.. note::

    A more advanced version of this script is mentioned in :ref:`aiohttp-demos-polls-preparations-database` notes.


Install both the ``asyncpg`` and ``sqlalchemy`` packages to interact with the database,
and run the script::

    $ pip install asyncpg
    $ pip install SQLAlchemy>=2
    $ python init_db.py

.. note::

    At this point we are not using any async features of the package. For this
    reason, you could have installed ``psycopg2`` package. Though since we are
    using sqlalchemy, we also could switch the type of database server.

Now there should be one record for *question* with related *choice* options
stored in corresponding tables in the database.

Use ``psql``, ``pgAdmin`` or any other tool you like to check database contents:

.. code-block:: text

    $ psql -U postgres -h localhost -p 5432 -d aiohttpdemo_polls
    aiohttpdemo_polls=# select * from question;
     id | question_text |  pub_date
    ----+---------------+------------
      1 | What's new?   | 2015-12-15
    (1 row)



Doing things at startup and shutdown
------------------------------------

Sometimes it is necessary to configure some component's setup and tear down.
For a database this would be the creation of a connection or connection pool and closing it afterwards.

Pieces of code below belong to ``aiohttpdemo_polls/db.py`` and ``aiohttpdemo_polls/main.py`` files.
Complete files will be shown shortly after.

.. _aiohttp-demos-polls-creating-connection-engine:

Creating connection engine
^^^^^^^^^^^^^^^^^^^^^^^^^^

For making DB queries we need an engine instance. Assuming ``conf`` is
a :class:`dict` with the configuration info for a Postgres connection, this
could be done by the following generator function:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/db.py
  :pyobject: pg_context

Add the code to ``aiohttpdemo_polls/db.py`` file.


The best place for connecting to the DB is using the
:attr:`~aiohtp.web.Application.cleanup_ctx` signal::

    app.cleanup_ctx.append(pg_context)

On startup, the code is run until the ``yield``. When the application is
shutdown the code will resume and close the DB connection.

.. note::

    We could also have used separate startup/shutdown functions with the
    :attr:`~aiohtp.web.Application.on_startup` and
    :attr:`~aiohtp.web.Application.on_cleanup` signals. However, a
    cleanup context ties the 2 parts together so that the DB can be
    correctly shutdown even if an error occurs in another startup step.


Complete files with changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    from sqlalchemy import MetaData, ForeignKey, String
    from sqlalchemy.orm import declarative_base, Mapped, mapped_column
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from datetime import date

    Base = declarative_base()

    class Question(Base):
        __tablename__ = "question"

        id: Mapped[int] = mapped_column(primary_key=True)
        question_text: Mapped[str] = mapped_column(String(200), nullable=False)
        pub_date: Mapped[date]

    class Choice(Base):
        __tablename__ = "choice"

        id: Mapped[int] = mapped_column(primary_key=True)
        choice_text: Mapped[str] = mapped_column(String(200), nullable=False)
        votes: Mapped[int] = mapped_column(server_default="0", nullable=False)

        question_id: Mapped[int] = mapped_column(
            ForeignKey("question.id", ondelete="CASCADE")
        )
        
    DSN = "postgresql+asyncgp://{user}:{password}@{host}:{port}/{database}"

        async def pg_context(app):
            engine = await create_async_engine(DSN.format(**app['config']['postgres']))
            app["db"] = async_sessionmaker(engine)

            yield

            await engine.dispose()

.. code-block:: python

    from aiohttp import web

    from settings import config
    from routes import setup_routes
    from db import pg_context

    app = web.Application()
    app["config"] = config
    setup_routes(app)
    app.cleanup_ctx.append(pg_context)
    web.run_app(app)


Since we now have database connection on start - let's use it! Modify index view:

.. code-block:: python

    # aiohttpdemo_polls/views.py
    from aiohttp import web
    from sqlalchemy import select
    import db


    async def index(request):
        async with request.app["db"]() as sess:
            rows = await sess.scalars(select(db.Question))
            questions = [f"{q.id}) {q.pub_date} : {q.question_text}" for q in rows.all()]
            return web.Response(text="\n".join(questions))


Run server and you should get list of available questions (one record at the moment) with all fields.


.. _aiohttp-demos-polls-templates:

Templates
---------

For setting up the template engine, we install the ``aiohttp_jinja2``
library first:

.. code-block:: shell

   $ pip install aiohttp_jinja2


After installing, setup the library:

.. code-block:: python
    :emphasize-lines: 3, 4, 12, 13

    # aiohttpdemo_polls/main.py
    from aiohttp import web
    import aiohttp_jinja2
    import jinja2

    from settings import config, BASE_DIR
    from routes import setup_routes
    from db import pg_context

    app = web.Application()
    app["config"] = config
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader(str(BASE_DIR / "aiohttpdemo_polls" / "templates")))
    setup_routes(app)
    app.cleanup_ctx.append(pg_context)
    web.run_app(app)


As you can see from setup above - templates should be placed at ``aiohttpdemo_polls/templates`` folder.

Below is the code for ``base.html``. The rest of the templates we're going to use are available `here`_.

.. _here: https://github.com/aio-libs/aiohttp-demos/tree/master/demos/polls/aiohttpdemo_polls/templates

.. code-block:: jinja

    <!--aiohttpdemo_polls/templates/base.html-->
    <!DOCTYPE html>
    <html>
      <head>
        {% block head %}
         <link rel="stylesheet" type="text/css" 
              href="{{ url('static', filename='style.css') }}" />
            <title>{{title}}</title>
        {% endblock %}
      </head>
      <body>
        <h1>{{title}}</h1>
        <div>
          {% block content %}
          {% endblock %}
        </div>
      </body>
    </html>


Let's create simple template and modify index view to use it:

.. code-block:: jinja

    <!--aiohttpdemo_polls/templates/index.html-->
    {% set title = "Main" %}

    {% if questions %}
        <ul>
        {% for question in questions %}
            <li>{{ question.question_text }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No questions are available.</p>
    {% endif %}


Templates are a very convenient way for web page writing. If we return a
dict with page content, the ``aiohttp_jinja2.template`` decorator
processes the dict using the jinja2 template renderer.

.. code-block:: python
    :emphasize-lines: 6, 10

    import aiohttp_jinja2
    from aiohttp import web
    from sqlalchemy import select
    import db


    @aiohttp_jinja2.template("index.html")
    async def index(request):
        async with request.app["db"]() as sess:
            questions = await sess.scalars(select(db.Question))
            return {"questions": questions.all()}

Run the server and you should see a question decorated in html list element.


Now let's add more views:

Update ``views.py`` and ``db.py`` one last time, to:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/views.py
  :pyobject: poll


Add the following to ``routes.py``:

.. code-block:: python

    app.router.add_get("/poll/{question_id}", poll, name="poll")
    app.router.add_get("/poll/{question_id}/results",
                       results, name="results")
    app.router.add_post("/poll/{question_id}/vote", vote, name="vote")

.. note::
    
    Don't forget to import ``poll, result, vote`` from ``views``.


You're now ready to add votes to your current question. Since we only have one, it can be accessed by adding ``/poll/1`` to our URL. This will allow you to cast a vote and, on submission, allow to check the updated poll.


.. _aiohttp-demos-polls-static-files:

Static files
------------

Any web site has static files such as: images, JavaScript sources, CSS files

The best way to handle static files in production is by setting up a reverse
proxy like NGINX or using CDN services.

During development, handling static files using the aiohttp server is very
convenient.

Fortunately, this can be easily done:

First we update ``routes.py``, adding:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/routes.py
  :pyobject: setup_static_routes

where ``project_root`` is the path to the root folder.

Then we update ``base.html``:

.. code-block:: jinja

    <!--aiohttpdemo_polls/templates/base.html-->
    <!DOCTYPE html>
    <html>
      <head>
        {% block head %}
         <link rel="stylesheet" type="text/css" 
              href="{{ url('static', filename='style.css') }}" />
            <title>{{title}}</title>
        {% endblock %}
      </head>
      <body>
        <h1>{{title}}</h1>
        <div>
          {% block content %}
          {% endblock %}
        </div>
      </body>
    </html>
    
Lastly, we import and call ``setup_static_routes`` in ``main.py``:

.. code-block:: python
    
    from routes import setup_static_routes
    
    setup_static_routes(app)



.. _aiohttp-demos-polls-middlewares:

Middlewares
-----------

Middlewares are stacked around every web-handler. They are called
before the handler for a pre-processing request. After getting
a response back, they are used for post-processing the given response.

A common use of middlewares is to implement custom error pages. Example from
:ref:`aiohttp-web-middlewares` documentation will render 404 errors using a
JSON response, as might be appropriate for a REST service.

Here we'll create a little bit more complex middleware custom display pages
for *404 Not Found* and *500 Internal Error*.

Every middleware should accept two parameters, a *request* and a *handler*,
and return the *response*. Middleware itself is a *coroutine* that can modify
either request or response:

Now, create a new ``middlewares.py`` file:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/middlewares.py

As you can see, we do nothing *before* the web handler. In the case of an ``HTTPException``,
we use the Jinja2 template renderer based on ``ex.status`` *after* the request was handled.
For other exceptions, we log the error and render our 500 template. Without the
``create_error_middleware`` function, the same task would take us many more ``if`` statements.

We have registered middleware in ``app`` by adding it to ``app.middlewares``.

Now, import and add a ``setup_middlewares`` step to the main file:

.. literalinclude:: ../demos/polls/aiohttpdemo_polls/main.py

Run the app again. To test, try an invalid url.

More
----

Ready to build a production app?

- Take a look at how to write tests: :ref:`aiohttp-testing`
- Consider enabling handler cancellation: :ref:`aiohttp-web-peer-disconnection`
- Deploy your app: :ref:`aiohttp-deployment`
