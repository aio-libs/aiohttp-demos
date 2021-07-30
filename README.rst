=============
aiohttp-demos
=============

.. image:: https://github.com/aio-libs/aiohttp-demos/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/aio-libs/aiohttp-demos/actions/workflows/ci.yml
   :alt: GitHub Actions status for master branch
.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/aio-libs/Lobby
    :alt: Chat on Gitter
.. image:: https://readthedocs.org/projects/aiohttp-demos/badge/?version=latest
   :target: http://aiohttp-demos.readthedocs.io/en/latest/
   :alt: Latest Read The Docs


Demos for `aiohttp <https://aiohttp.readthedocs.io>`_ project.


.. contents::

Imagetagger Deep Learning Image Classifier
------------------------------------------
Example how to deploy deep learning model with aiohttp.

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp-demos/master/docs/_static/imagetagger.png


URL shortener
-------------
Simple URL shortener with Redis storage.

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp-demos/master/docs/_static/shorty.png


Toxic Comments Classifier
-------------------------
UI and API for classification of offensive and toxic comments using Kaggle data and simple
logistic regression.

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp-demos/master/docs/_static/moderator.png


Moderator Slack Bot
-------------------
Slack bot that moderates offensive and toxic chat messages using model from `Moderator AI`.

.. image:: /docs/_static/slack_moderator.gif
    :align: center
    :width: 460px


Twitter clone
-------------
Twitter clone with MongoDB storage.

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp-demos/master/docs/_static/motortwit.png


Chat
----
Simple chat using websockets.

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp-demos/master/docs/_static/chat.png


Polls app
---------
Simple *polls* application with PostgreSQL storage.

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp-demos/master/docs/_static/polls.png
    :align: center
    :width: 460px


Blog
----
Blog application with PostgreSQL storage and Redis session store.

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp-demos/master/docs/_static/blog.png
    :align: center
    :width: 460px



GraphQL Messenger
-----------------
The simple realization of the GraphQL api.

.. image:: /docs/_static/graph.gif
    :align: center
    :width: 460px


Contributing
------------
Things you need for local development::

    $ pip install -r requirements-dev.txt
    $ pip install demos/polls
    $ pip install demos/chat
    $ pip install demos/blog
    $ pip install demos/graphql-demo


To check documentation locally - run::

    $ make doc

and click the ``open file`` link from the output.


To make sure everything is ok before committing::

    $ make ci


Improvement plan
----------------

Polls:

- [+] create configuration steps (venv, pip install, db initialization)
- [+] fix or recreate tests
- [~] revise `tutorial.rst`
- [+] fix urls from `aiohttp/tutorial`
- [x] setup communication channels (aio-libs gitter channel is enough)
- [~] create missing issues
- [+] add "Contributing" section
- [ ] add "What's next" section
- [ ] discuss roadmap
