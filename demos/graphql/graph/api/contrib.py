from aiohttp import web
from aiohttp_graphql import GraphQLView
from graphql_ws.aiohttp import AiohttpSubscriptionServer
from aiohttp_graphql.render_graphiql import (
    GRAPHIQL_VERSION,
    process_var,
)


GQPHIQL_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <style>
    html, body {
      height: 100%;
      margin: 0;
      overflow: hidden;
      width: 100%;
    }
  </style>
  <meta name="referrer" content="no-referrer">
  <link
    href="//cdn.jsdelivr.net/graphiql/{{graphiql_version}}/graphiql.css"
    rel="stylesheet"
  />
  <script src="//cdn.jsdelivr.net/fetch/0.9.0/fetch.min.js"></script>
  <script src="//cdn.jsdelivr.net/react/15.0.0/react.min.js"></script>
  <script src="//cdn.jsdelivr.net/react/15.0.0/react-dom.min.js"></script>
  <script
    src="//cdn.jsdelivr.net/graphiql/{{graphiql_version}}/graphiql.min.js"
  >
  </script>
  <script src="//unpkg.com/subscriptions-transport-ws@0.7.0/browser/client.js">
  </script>
  <script
    src="//unpkg.com/graphiql-subscriptions-fetcher@0.0.2/browser/client.js"
  >
  </script>
</head>
<body>
  <script>
    // Collect the URL parameters
    var parameters = {};
    window.location.search.substr(1).split('&').forEach(function (entry) {
      var eq = entry.indexOf('=');
      if (eq >= 0) {
        parameters[decodeURIComponent(entry.slice(0, eq))] =
          decodeURIComponent(entry.slice(eq + 1));
      }
    });

    // Produce a Location query string from a parameter object.
    function locationQuery(params) {
      return '?' + Object.keys(params).map(function (key) {
        return encodeURIComponent(key) + '=' +
          encodeURIComponent(params[key]);
      }).join('&');
    }

    // Derive a fetch URL from the current URL, sans the GraphQL parameters.
    var graphqlParamNames = {
      query: true,
      variables: true,
      operationName: true
    };

    var otherParams = {};
    for (var k in parameters) {
      if (parameters.hasOwnProperty(k) && graphqlParamNames[k] !== true) {
        otherParams[k] = parameters[k];
      }
    }

    var subscriptionsClient =
        new window.SubscriptionsTransportWs.SubscriptionClient('{{socket}}', {
            reconnect: true
        });
    var fetcher = window.GraphiQLSubscriptionsFetcher.graphQLFetcher(
        subscriptionsClient, graphQLFetcher
    );
    var fetchURL = locationQuery(otherParams);

    // Defines a GraphQL fetcher using the fetch API.
    function graphQLFetcher(graphQLParams) {
      return fetch(fetchURL, {
        method: 'post',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(graphQLParams),
        credentials: 'include',
      }).then(function (response) {
        return response.text();
      }).then(function (responseBody) {
        try {
          return JSON.parse(responseBody);
        } catch (error) {
          return responseBody;
        }
      });
    }

    // When the query and variables string is edited, update the URL bar so
    // that it can be easily shared.
    function onEditQuery(newQuery) {
      parameters.query = newQuery;
      updateURL();
    }

    function onEditVariables(newVariables) {
      parameters.variables = newVariables;
      updateURL();
    }

    function onEditOperationName(newOperationName) {
      parameters.operationName = newOperationName;
      updateURL();
    }

    function updateURL() {
      history.replaceState(null, null, locationQuery(parameters));
    }

    // Render <GraphiQL /> into the body.
    ReactDOM.render(
      React.createElement(GraphiQL, {
        fetcher: fetcher,
        onEditQuery: onEditQuery,
        onEditVariables: onEditVariables,
        onEditOperationName: onEditOperationName,
        query: {{query|tojson}},
        response: {{result|tojson}},
        variables: {{variables|tojson}},
        operationName: {{operation_name|tojson}},
      }),
      document.body
    );
  </script>
</body>
</html>
'''


def simple_renderer(template, **values):
    replace = ['graphiql_version', 'socket', ]
    replace_jsonify = ['query', 'result', 'variables', 'operation_name']

    for rep in replace:
        template = process_var(template, rep, values.get(rep, ''))

    for rep in replace_jsonify:
        template = process_var(template, rep, values.get(rep, ''), True)

    return template


class CustomGraphQLView(GraphQLView):

    def __init__(self, *args, socket=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket

    async def render_graphiql(self, params, result):
        template_vars = {
            'graphiql_version': GRAPHIQL_VERSION,
            'query': params and params.query,
            'variables': params and params.variables,
            'operation_name': params and params.operation_name,
            'result': result,
            'socket': self.socket,
        }

        source = simple_renderer(GQPHIQL_TEMPLATE, **template_vars)

        return web.Response(text=source, content_type='text/html')


class CustomAiohttpSubscriptionServer(AiohttpSubscriptionServer):

    def get_graphql_params(self, connection_context, *args, **kwargs):
        params = super().get_graphql_params(
            connection_context,
            *args,
            **kwargs,
        )
        params.update({'context_value': connection_context.request_context})

        return params
