Imagetagger Keras Demo
======================

Simple application how to use aiohttp_ for deep learning project with keras_.

**Imagetagger** is API for image recognition, employs mobilenet_ network to
classify images, but other supported network can be used.


Install the app::

    $ git clone https://github.com/aio-libs/aiohttp-keras-demo.git
    $ cd aiohttp-keras-demo
    $ pip install -r requirements/development.txt


Run application::

    $ make run


Example of request::

    curl -F file=@tests/data/aircraft.jpg http://localhost:8000/predict

Example of response::

    {"predictions": [
        {"label": "envelope", "probability": 0.3094555735588074},
        {"label": "airship", "probability": 0.20662210881710052},
        {"label": "carton", "probability": 0.07820204645395279},
        {"label": "freight_car", "probability": 0.056770652532577515},
        {"label": "airliner", "probability": 0.04821280017495155}],
    "success": true}


Requirements
============
* Python3.6
* aiohttp_
* keras_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _keras: https://keras.io/
.. _mobilenet: https://keras.io/applications/#mobilenet
