# GraphQl Messenger

The simple realization of GraphQl api.
- query
- mutations
- subscriptions

![Image of Application](/docs/_static/graph.gif)


### Install requirements:
```
$ cd graphql-demo
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

### Others

```
make test # running tests
make lint # running the flake8
make mypy # running the types checking by mypy

```

### Requirements
- aiohttp
- aiopg
- aioredis
- graphene
