Moderator AI Demo
=================
.. image:: https://travis-ci.org/jettify/moderator.ai.svg?branch=master
    :target: https://travis-ci.org/jettify/moderator.ai


.. image:: https://raw.githubusercontent.com/jettify/moderator.ai/master/docs/preview.png

Simple application how to use aiohttp_ for machine learning project. Project is
API and UI for classification of toxic and offensive comments, based on data
from kaggle_ competition. Project can be used as example how to separate CPU
intensive tasks from blocking event loop.


Install the app::

    $ cd moderator
    $ pip install -r requirements-dev.txt


Run application::

    $ make run

Open browser::

    http://127.0.0.1:9001


Requirements
============
* aiohttp_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _kaggle: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge
