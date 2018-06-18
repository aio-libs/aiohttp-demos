# GraphQl Messenger

The simple realization of GraphQl api.

![Image of Application](/docs/_static/graph.gif)


### Install requirements:
```
$ cd graph
$ pip install -r requirements-dev.txt
$ pip install -e .
```

### Run application:
```
$ make start_database
$ make start_redis
$ make prepare_database
$ make
```
### Open in browser:
```
$ open http://0.0.0.0:8080/
$ open http://0.0.0.0:8080/graphiql
```