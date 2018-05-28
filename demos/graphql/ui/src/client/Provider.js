import React from 'react';
import { ApolloProvider } from 'react-apollo';
import client from './';

export default function AppProvider({ children }) {
  return (
    <ApolloProvider client={client}>
      <div>
        {children}
      </div>
    </ApolloProvider>
  );
}
