import ApolloClient, { createNetworkInterface } from 'apollo-client';
import {
  SubscriptionClient,
  addGraphQLSubscriptions
} from 'subscriptions-transport-ws';

const wsClient = new SubscriptionClient('ws://localhost:8080/subscriptions');
const baseNetworkInterface = createNetworkInterface({
  uri: '/graphql',
});
const subscriptionNetworkInterface = addGraphQLSubscriptions(
  baseNetworkInterface,
  wsClient,
  );


export default new ApolloClient({
  networkInterface: subscriptionNetworkInterface,
  connectToDevTools: true,
});
