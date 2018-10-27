=============
aiohttp-demos
=============

.. image:: https://travis-ci.org/aio-libs/aiohttp-demos.svg?branch=master
    :target: https://travis-ci.org/aio-libs/aiohttp-demos
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

After that, follow setup instructions from a particular demo project.

To check documentation locally click the ``open file`` link from the output
of this command::

    $ make doc

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
