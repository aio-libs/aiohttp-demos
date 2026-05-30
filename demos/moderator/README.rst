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


Trust boundary for the pickled model
====================================

The demo loads its trained scikit-learn pipeline by calling
``pickle.load`` on ``model/pipeline.dat`` at worker startup
(see ``moderator/worker.py::warm``). ``pickle.load`` will execute
arbitrary Python code embedded in the pickle stream, so the file at
``model_path`` must be treated as trusted application data: anyone
who can replace or modify it can run code inside the worker process
at startup.

In practice that means:

* Do not extend this demo to accept model uploads from HTTP clients
  and feed them to ``pickle.load``.
* If you are packaging this for a real deployment, pin
  ``model/pipeline.dat`` to a known-good build artifact (e.g. ship
  it inside the container image, or verify a checksum/signature
  before loading) and make sure the filesystem path is not writable
  by untrusted processes.
* If you want to support user-supplied or downloaded models, switch
  to a safer serialization format (e.g. ``joblib`` with integrity
  checking, ``skops``, or a model registry that signs artifacts)
  rather than raw ``pickle``.


Requirements
============
* aiohttp_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _kaggle: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge
